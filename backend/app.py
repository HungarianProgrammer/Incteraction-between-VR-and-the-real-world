import os
from flask import Flask, jsonify
from flask_cors import CORS
from blueprints.mqtt import mqtt_bp
from blueprints.mqtt.routes import initialize_mqtt_client

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configure app from environment variables
    app.config.from_mapping(
        BROKER_ADDRESS=os.environ.get('BROKER_ADDRESS', 'localhost'),
        BROKER_PORT=int(os.environ.get('BROKER_PORT', 9001)),
        USE_WEBSOCKETS=os.environ.get('USE_WEBSOCKETS', 'true').lower() == 'true',
        DEBUG=os.environ.get('FLASK_DEBUG', 'true').lower() == 'true',
    )
    
    # Override config with test config if provided
    if test_config:
        app.config.update(test_config)
        
    # Setup CORS
    CORS(app, origins=os.environ.get('CORS_ORIGINS', "*"))
    
    # Register the MQTT blueprint
    app.register_blueprint(mqtt_bp, url_prefix='/api/mqtt')
    
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            "message": "Health", 
            "status": "OK",
            "version": "1.0.0"
        }), 200 
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found."}), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error."}), 500
        
    # Initialize the MQTT client with app configuration
    with app.app_context():
        initialize_mqtt_client(app)
        
    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=app.config['DEBUG'])