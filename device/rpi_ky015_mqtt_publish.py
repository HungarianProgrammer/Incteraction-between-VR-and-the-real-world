#!/usr/bin/env python3
import time
import sys
import threading
import os
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import dht11

# === Load Configuration from Environment Variables ===
# Get environment variables with defaults
BROKER_ADDRESS = os.environ.get("BROKER_ADDRESS", "localhost")
BROKER_PORT = int(os.environ.get("BROKER_PORT", "8080"))
USE_WEBSOCKETS = os.environ.get("USE_WEBSOCKETS", "true").lower() == "true"

TEMP_TOPIC = os.environ.get("TEMP_TOPIC", "sensors/temperature")
HUMIDITY_TOPIC = os.environ.get("HUMIDITY_TOPIC", "sensors/humidity")
CONTROL_TOPIC = os.environ.get("CONTROL_TOPIC", "light")
MOTION_TOPIC = os.environ.get("MOTION_TOPIC", "motion")

DHT_PIN = int(os.environ.get("DHT_PIN", "17"))
LIGHT_GPIO_PIN = int(os.environ.get("LIGHT_GPIO_PIN", "27"))
SERVO_PIN = int(os.environ.get("SERVO_PIN", "24"))
READ_INTERVAL = int(os.environ.get("READ_INTERVAL", "2"))

# Print configuration
print("\n=== Configuration ===")
print(f"BROKER_ADDRESS: {BROKER_ADDRESS}")
print(f"BROKER_PORT: {BROKER_PORT}")
print(f"USE_WEBSOCKETS: {USE_WEBSOCKETS}")
print(f"TEMP_TOPIC: {TEMP_TOPIC}")
print(f"HUMIDITY_TOPIC: {HUMIDITY_TOPIC}")
print(f"CONTROL_TOPIC: {CONTROL_TOPIC}")
print(f"MOTION_TOPIC: {MOTION_TOPIC}")
print(f"DHT_PIN: {DHT_PIN}")
print(f"LIGHT_GPIO_PIN: {LIGHT_GPIO_PIN}")
print(f"SERVO_PIN: {SERVO_PIN}")
print(f"READ_INTERVAL: {READ_INTERVAL}")
print("===================\n")

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_GPIO_PIN, GPIO.OUT)
GPIO.output(LIGHT_GPIO_PIN, GPIO.LOW)

GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)  
servo_pwm.start(7.5)

# === Helper: Move Servo ===
def set_servo_angle(angle):
    duty = 2.5 + (angle / 18.0)
    servo_pwm.ChangeDutyCycle(duty)
    print(f"Servo moved to {angle}°")
    time.sleep(0.5)
    servo_pwm.ChangeDutyCycle(0)

# === MQTT Callbacks ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(CONTROL_TOPIC)
        client.subscribe(MOTION_TOPIC)
        print(f"Subscribed to topics: {CONTROL_TOPIC}, {MOTION_TOPIC}")
    else:
        print(f"Failed to connect: code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip().lower()
    topic = msg.topic
    print(f"Received on '{topic}': {payload}")

    if topic == CONTROL_TOPIC:
        if payload == "on":
            GPIO.output(LIGHT_GPIO_PIN, GPIO.HIGH)
            print("Light turned ON")
        elif payload == "off":
            GPIO.output(LIGHT_GPIO_PIN, GPIO.LOW)
            print("Light turned OFF")
        else:
            print("Unknown light command")

    elif topic == MOTION_TOPIC:
        if payload.startswith("left ") or payload.startswith("right "):
            try:
                parts = payload.split()
                direction, value = parts[0], int(parts[1])
                if 0 <= value <= 90:
                    angle = 90 - value if direction == "left" else 90 + value
                    angle = max(0, min(180, angle))
                    set_servo_angle(angle)
                else:
                    print("Angle out of range (0–90 from center)")
            except Exception as e:
                print(f"Invalid motion command: {e}")
        else:
            print("Unknown motion command")

# === Sensor Reading and Publishing ===
def sensor_loop(client):
    print(f"Starting sensor publishing every {READ_INTERVAL} seconds...")
    sensor = dht11.DHT11(pin=DHT_PIN)
    while True:
        result = sensor.read()
        if result.is_valid():
            temperature = result.temperature
            humidity = result.humidity
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
            client.publish(TEMP_TOPIC, str(temperature))
            client.publish(HUMIDITY_TOPIC, str(humidity))
        else:
            print("Sensor read failed. Retrying...")
        time.sleep(READ_INTERVAL)

# === Main Function ===
def main():
    client = mqtt.Client(transport="websockets" if USE_WEBSOCKETS else "tcp")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
        client.loop_start()

        sensor_thread = threading.Thread(target=sensor_loop, args=(client,))
        sensor_thread.daemon = True
        sensor_thread.start()

        print("Press Ctrl+C to exit")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExiting program...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.output(LIGHT_GPIO_PIN, GPIO.LOW)
        servo_pwm.stop()
        GPIO.cleanup()
        client.loop_stop()
        client.disconnect()
        print("Cleaned up and disconnected")

if __name__ == "__main__":
    main()