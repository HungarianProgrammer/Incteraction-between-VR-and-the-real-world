#!/bin/bash

echo "Starting MQTT Light Control Script"
echo "Configuration from environment variables:"
echo "BROKER_ADDRESS: $BROKER_ADDRESS"
echo "BROKER_PORT: $BROKER_PORT"
echo "CONTROL_TOPIC (light control): $CONTROL_TOPIC"

# Run the Python script - it will read environment variables directly
python3 /app/rpi_ky015_mqtt_publish.py