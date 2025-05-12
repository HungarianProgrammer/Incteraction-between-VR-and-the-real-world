import time
from datetime import datetime
from flask import jsonify, current_app, request
import paho.mqtt.client as mqtt
from . import mqtt_bp
from models import db, TemperatureData, HumidityData

# Global variables to store the latest sensor data
temperature_data = {"value": 0, "timestamp": 0}
humidity_data = {"value": 0, "timestamp": 0}
light_status = {"state": "off", "timestamp": 0}
motion_status = {"direction": "center", "angle": 0, "timestamp": 0}
connection_status = {"connected": False, "last_message": 0}
subscriptions = {"temperature": False, "humidity": False, "light": False, "motion": False}

# MQTT client instance
client = None

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects to the MQTT broker"""
    if rc == 0:
        print("Connected to MQTT broker")
        connection_status["connected"] = True
        # Subscribe to temperature, humidity, light, and motion topics
        client.subscribe("sensors/temperature")
        client.subscribe("sensors/humidity")
        client.subscribe("light")
        client.subscribe("motion")
        print("Subscribed to sensors/temperature, sensors/humidity, light, and motion topics")
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")
        connection_status["connected"] = False

def on_subscribe(client, userdata, mid, granted_qos):
    """Callback for when the client successfully subscribes to a topic"""
    print(f"Successfully subscribed with message ID: {mid}")
    # Note: We can't directly map mid to specific topics here, but this confirms subscriptions are working

def on_message(client, userdata, msg):
    """Callback for when a message is received from the MQTT broker"""
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    current_time = time.time()
    
    if topic == "light":
        # Handle light control messages
        payload_lower = payload.strip().lower()
        if payload_lower in ["on", "off"]:
            light_status["state"] = payload_lower
            light_status["timestamp"] = current_time
            subscriptions["light"] = True
            connection_status["last_message"] = current_time
            print(f"Received light control command: {payload}")
        else:
            print(f"Received invalid light command: {payload}")
        return
    
    if topic == "motion":
        # Handle motion control messages
        payload_lower = payload.strip().lower()
        try:
            parts = payload_lower.split()
            if len(parts) >= 2 and parts[0] in ["left", "right"]:
                direction = parts[0]
                angle = int(parts[1])
                if 0 <= angle <= 90:
                    motion_status["direction"] = direction
                    motion_status["angle"] = angle
                    motion_status["timestamp"] = current_time
                    subscriptions["motion"] = True
                    connection_status["last_message"] = current_time
                    print(f"Received motion control command: {direction} {angle}")
                else:
                    print(f"Received invalid motion angle (must be 0-90): {angle}")
            else:
                print(f"Received invalid motion format: {payload}")
        except (ValueError, IndexError) as e:
            print(f"Error parsing motion command '{payload}': {str(e)}")
        return
    
    try:
        value = float(payload)
        if topic == "sensors/temperature":
            temperature_data["value"] = value
            temperature_data["timestamp"] = current_time
            subscriptions["temperature"] = True
            
            # Store in database
            try:
                new_temp = TemperatureData(value=value, timestamp=datetime.utcfromtimestamp(current_time))
                db.session.add(new_temp)
                db.session.commit()
                print(f"Temperature data stored in database: {value}°C")
            except Exception as e:
                print(f"Error storing temperature data: {str(e)}")
                db.session.rollback()
                
        elif topic == "sensors/humidity":
            humidity_data["value"] = value
            humidity_data["timestamp"] = current_time
            subscriptions["humidity"] = True
            
            # Store in database
            try:
                new_humidity = HumidityData(value=value, timestamp=datetime.utcfromtimestamp(current_time))
                db.session.add(new_humidity)
                db.session.commit()
                print(f"Humidity data stored in database: {value}%")
            except Exception as e:
                print(f"Error storing humidity data: {str(e)}")
                db.session.rollback()
            
        connection_status["last_message"] = current_time
        print(f"Received message on topic {topic}: {payload}")
    except ValueError:
        print(f"Received invalid data on topic {topic}: {payload}")

def initialize_mqtt_client(app):
    """Initialize the MQTT client with the broker settings"""
    global client
    
    broker_address = "localhost"
    broker_port = 8080  # WebSocket port as per your configuration
    
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    
    # Connect to the MQTT broker
    try:
        client.connect(broker_address, broker_port, 60)
        # Start the MQTT client loop in a non-blocking way
        client.loop_start()
        print(f"MQTT client initialized and connecting to {broker_address}:{broker_port}")
    except Exception as e:
        print(f"Failed to initialize MQTT client: {str(e)}")
        
@mqtt_bp.route('/temperature', methods=['GET'])
def get_temperature():
    """Endpoint to get the latest temperature data"""
    if time.time() - temperature_data["timestamp"] > 300:  # Data older than 5 minutes
        return jsonify({"error": "Temperature data is stale or not available"}), 404
    
    return jsonify({
        "temperature": temperature_data["value"],
        "timestamp": temperature_data["timestamp"]
    }), 200

@mqtt_bp.route('/temperature/history', methods=['GET'])
def get_temperature_history():
    """Endpoint to get historical temperature data"""
    try:
        # Get optional query parameters
        limit = request.args.get('limit', default=100, type=int)
        start_time = request.args.get('start_time', default=None, type=float)
        end_time = request.args.get('end_time', default=None, type=float)
        
        # Build the query
        query = TemperatureData.query
        
        # Apply time filters if provided
        if start_time:
            start_datetime = datetime.utcfromtimestamp(start_time)
            query = query.filter(TemperatureData.timestamp >= start_datetime)
            
        if end_time:
            end_datetime = datetime.utcfromtimestamp(end_time)
            query = query.filter(TemperatureData.timestamp <= end_datetime)
        
        # Order by timestamp descending and limit results
        temperature_records = query.order_by(TemperatureData.timestamp.desc()).limit(limit).all()
        
        # Convert to list of dictionaries
        data = [record.to_dict() for record in temperature_records]
        
        return jsonify({
            "count": len(data),
            "data": data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mqtt_bp.route('/humidity', methods=['GET'])
def get_humidity():
    """Endpoint to get the latest humidity data"""
    if time.time() - humidity_data["timestamp"] > 300:  # Data older than 5 minutes
        return jsonify({"error": "Humidity data is stale or not available"}), 404
    
    return jsonify({
        "humidity": humidity_data["value"],
        "timestamp": humidity_data["timestamp"]
    }), 200

@mqtt_bp.route('/humidity/history', methods=['GET'])
def get_humidity_history():
    """Endpoint to get historical humidity data"""
    try:
        # Get optional query parameters
        limit = request.args.get('limit', default=100, type=int)
        start_time = request.args.get('start_time', default=None, type=float)
        end_time = request.args.get('end_time', default=None, type=float)
        
        # Build the query
        query = HumidityData.query
        
        # Apply time filters if provided
        if start_time:
            start_datetime = datetime.utcfromtimestamp(start_time)
            query = query.filter(HumidityData.timestamp >= start_datetime)
            
        if end_time:
            end_datetime = datetime.utcfromtimestamp(end_time)
            query = query.filter(HumidityData.timestamp <= end_datetime)
        
        # Order by timestamp descending and limit results
        humidity_records = query.order_by(HumidityData.timestamp.desc()).limit(limit).all()
        
        # Convert to list of dictionaries
        data = [record.to_dict() for record in humidity_records]
        
        return jsonify({
            "count": len(data),
            "data": data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@mqtt_bp.route('/light', methods=['GET'])
def get_light_status():
    """Endpoint to get the latest light status"""
    if time.time() - light_status["timestamp"] > 300:  # Data older than 5 minutes
        return jsonify({"error": "Light status is stale or not available"}), 404
    
    return jsonify({
        "state": light_status["state"],
        "timestamp": light_status["timestamp"]
    }), 200

@mqtt_bp.route('/light', methods=['POST'])
def control_light():
    """Endpoint to control the light via MQTT"""
    global client
    
    if not client or not connection_status["connected"]:
        return jsonify({"error": "MQTT client is not connected"}), 503
    
    data = request.json
    state = data.get('state', '').strip().lower()
    
    if state not in ["on", "off"]:
        return jsonify({"error": "Invalid state. Must be 'on' or 'off'"}), 400
    
    try:
        # Publish the light control command
        result = client.publish("light", state)
        if result.rc == 0:
            # Update local state immediately for faster response
            light_status["state"] = state
            light_status["timestamp"] = time.time()
            
            return jsonify({
                "success": True, 
                "message": f"Light turned {state}",
                "state": state
            }), 200
        else:
            return jsonify({"success": False, "error": f"Failed to publish with code {result.rc}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@mqtt_bp.route('/status', methods=['GET'])
def get_status():
    """Endpoint to check the MQTT connection status"""
    is_active = connection_status["connected"] and (time.time() - connection_status["last_message"] < 300)
    
    return jsonify({
        "connected": connection_status["connected"],
        "active": is_active,
        "last_message_time": connection_status["last_message"],
        "subscriptions": {
            "temperature_received": subscriptions["temperature"],
            "humidity_received": subscriptions["humidity"],
            "light_received": subscriptions["light"],
            "motion_received": subscriptions["motion"]
        }
    }), 200

@mqtt_bp.route('/publish', methods=['POST'])
def publish_test_data():
    """Endpoint to manually publish test data to MQTT topics for debugging"""
    global client
    
    if not client or not connection_status["connected"]:
        return jsonify({"error": "MQTT client is not connected"}), 503
    
    data = request.json
    topic = data.get('topic')
    value = data.get('value')
    
    if not topic or value is None:
        return jsonify({"error": "Topic and value are required"}), 400
    
    try:
        # Publish the test data
        result = client.publish(topic, str(value))
        if result.rc == 0:
            return jsonify({"success": True, "message": f"Published {value} to {topic}"}), 200
        else:
            return jsonify({"success": False, "error": f"Failed to publish with code {result.rc}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@mqtt_bp.route('/motion', methods=['GET'])
def get_motion_status():
    """Endpoint to get the latest motion status"""
    if time.time() - motion_status["timestamp"] > 300:  # Data older than 5 minutes
        return jsonify({"error": "Motion status is stale or not available"}), 404
    
    return jsonify({
        "direction": motion_status["direction"],
        "angle": motion_status["angle"],
        "timestamp": motion_status["timestamp"]
    }), 200

@mqtt_bp.route('/motion', methods=['POST'])
def control_motion():
    """Endpoint to control motion via MQTT"""
    global client
    
    if not client or not connection_status["connected"]:
        return jsonify({"error": "MQTT client is not connected"}), 503
    
    data = request.json
    direction = data.get('direction', '').strip().lower()
    angle = data.get('angle')
    
    # Validate direction
    if direction not in ["left", "right"]:
        return jsonify({"error": "Invalid direction. Must be 'left' or 'right'"}), 400
    
    # Validate angle
    try:
        angle = int(angle)
        if not (0 <= angle <= 90):
            return jsonify({"error": "Angle must be between 0 and 90 degrees"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Angle must be a number between 0 and 90"}), 400
    
    try:
        # Construct the motion command in the format expected by the Raspberry Pi
        motion_command = f"{direction} {angle}"
        
        # Publish the motion control command
        result = client.publish("motion", motion_command)
        if result.rc == 0:
            # Update local state immediately for faster response
            motion_status["direction"] = direction
            motion_status["angle"] = angle
            motion_status["timestamp"] = time.time()
            
            return jsonify({
                "success": True, 
                "message": f"Motion set to {direction} {angle}°",
                "direction": direction,
                "angle": angle
            }), 200
        else:
            return jsonify({"success": False, "error": f"Failed to publish with code {result.rc}"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@mqtt_bp.route('/stats', methods=['GET'])
def get_database_stats():
    """Endpoint to get statistics about the stored sensor data"""
    try:
        # Count records
        temperature_count = TemperatureData.query.count()
        humidity_count = HumidityData.query.count()
        
        # Get min, max, avg for temperature if records exist
        temp_stats = {}
        if temperature_count > 0:
            temp_min = db.session.query(db.func.min(TemperatureData.value)).scalar()
            temp_max = db.session.query(db.func.max(TemperatureData.value)).scalar()
            temp_avg = db.session.query(db.func.avg(TemperatureData.value)).scalar()
            
            # Get the newest and oldest record timestamps
            newest_temp = db.session.query(db.func.max(TemperatureData.timestamp)).scalar()
            oldest_temp = db.session.query(db.func.min(TemperatureData.timestamp)).scalar()
            
            temp_stats = {
                "min": temp_min,
                "max": temp_max,
                "avg": temp_avg,
                "first_record": oldest_temp.timestamp() if oldest_temp else None,
                "last_record": newest_temp.timestamp() if newest_temp else None
            }
        
        # Get min, max, avg for humidity if records exist
        humidity_stats = {}
        if humidity_count > 0:
            humidity_min = db.session.query(db.func.min(HumidityData.value)).scalar()
            humidity_max = db.session.query(db.func.max(HumidityData.value)).scalar()
            humidity_avg = db.session.query(db.func.avg(HumidityData.value)).scalar()
            
            # Get the newest and oldest record timestamps
            newest_humidity = db.session.query(db.func.max(HumidityData.timestamp)).scalar()
            oldest_humidity = db.session.query(db.func.min(HumidityData.timestamp)).scalar()
            
            humidity_stats = {
                "min": humidity_min,
                "max": humidity_max,
                "avg": humidity_avg,
                "first_record": oldest_humidity.timestamp() if oldest_humidity else None,
                "last_record": newest_humidity.timestamp() if newest_humidity else None
            }
        
        return jsonify({
            "temperature": {
                "count": temperature_count,
                "stats": temp_stats
            },
            "humidity": {
                "count": humidity_count,
                "stats": humidity_stats
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500