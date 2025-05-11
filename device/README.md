# Raspberry Pi MQTT Light Control

This project enables a Raspberry Pi to both monitor sensors and control actuators via MQTT. It creates an interactive bridge between a virtual reality environment and the physical world.

## Features

- **Temperature & Humidity Sensing**: Reads data from KY-015 (DHT11) sensor
- **Light Control**: Subscribes to MQTT "light" topic and controls an LED/relay
- **Motion Control**: Subscribes to MQTT "motion" topic to control a servo motor
- **Docker Support**: Easy deployment with configurable environment variables
- **Environment Variable Configuration**: All settings configurable via ENV vars

## Hardware Requirements

- Raspberry Pi (tested on Raspberry Pi 4)
- DHT11/KY-015 temperature and humidity sensor
- LED or relay module for light control
- Servo motor (optional)

## Wiring Setup

- **DHT11 Sensor**: Connect data pin to GPIO17 (pin 11)
- **Light Control**: Connect LED/relay to GPIO27 (pin 13)
- **Servo Motor**: Connect signal wire to GPIO24 (pin 18)

```
┌─────────────┐                ┌─────────┐
│             │                │         │
│  Raspberry  │                │  DHT11  │
│     Pi      │───GPIO17──────►│ Sensor  │
│             │                │         │
└─────────────┘                └─────────┘
       │
       │                      ┌─────────┐
       │                      │         │
       └────GPIO27───────────►│  Light  │
       │                      │         │
       │                      └─────────┘
       │
       │                      ┌─────────┐
       │                      │         │
       └────GPIO24───────────►│  Servo  │
                              │         │
                              └─────────┘
```

## Project Structure

- **rpi_ky015_mqtt_publish.py**: Main script that handles sensor reading and MQTT communication
- **Dockerfile**: Containerizes the application for easy deployment
- **entrypoint.sh**: Entry point script for the Docker container
- **requirements.txt**: Python dependencies

## Docker Setup and Usage

### Building the Docker Image

```bash
docker build -t rpi-mqtt-device .
```

### Running the Container

```bash
# Run with default settings
docker run --device /dev/gpiomem:/dev/gpiomem rpi-mqtt-device

# Run with custom broker address
docker run --device /dev/gpiomem:/dev/gpiomem -e BROKER_ADDRESS="custom.broker" rpi-mqtt-device
```

The `--device /dev/gpiomem:/dev/gpiomem` flag is needed to allow GPIO access from inside the container.

### Environment Variables

All configuration is done through environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| BROKER_ADDRESS | "localhost" | MQTT broker address |
| BROKER_PORT | 8080 | MQTT broker port |
| USE_WEBSOCKETS | true | Use WebSockets for MQTT (true/false) |
| TEMP_TOPIC | "sensors/temperature" | Topic for temperature data |
| HUMIDITY_TOPIC | "sensors/humidity" | Topic for humidity data |
| CONTROL_TOPIC | "light" | Topic for light control |
| MOTION_TOPIC | "motion" | Topic for servo control |
| DHT_PIN | 17 | GPIO pin for DHT11 sensor |
| LIGHT_GPIO_PIN | 27 | GPIO pin for light control |
| SERVO_PIN | 24 | GPIO pin for servo control |
| READ_INTERVAL | 2 | Seconds between sensor readings |

Example with multiple custom settings:

```bash
docker run \
  --device /dev/gpiomem:/dev/gpiomem \
  -e BROKER_ADDRESS="mqtt.example.com" \
  -e BROKER_PORT=1883 \
  -e USE_WEBSOCKETS=false \
  -e CONTROL_TOPIC="home/lights/livingroom" \
  -e MOTION_TOPIC="home/servo" \
  rpi-mqtt-device
```

## Running Without Docker

If you prefer to run directly on the Raspberry Pi:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   sudo python3 rpi_ky015_mqtt_publish.py
   ```

You can also use environment variables to configure the script directly:

```bash
BROKER_ADDRESS="mqtt.example.com" CONTROL_TOPIC="custom/light" sudo -E python3 rpi_ky015_mqtt_publish.py
```

## MQTT Topic Control Guide

### Light Control

To control the light, publish messages to the MQTT topic specified by `CONTROL_TOPIC` (default: "light"):

```bash
# Turn light ON
mosquitto_pub -h your.mqtt.broker -t light -m "on"

# Turn light OFF
mosquitto_pub -h your.mqtt.broker -t light -m "off"
```

### Servo Control

To control the servo, publish messages to the `MOTION_TOPIC` (default: "motion"):

```bash
# Move servo left 45 degrees from center
mosquitto_pub -h your.mqtt.broker -t motion -m "left 45"

# Move servo right 30 degrees from center
mosquitto_pub -h your.mqtt.broker -t motion -m "right 30"
```

## Sensor Data

The script publishes sensor data to the following topics:

- Temperature: Published to `TEMP_TOPIC` (default: "sensors/temperature")
- Humidity: Published to `HUMIDITY_TOPIC` (default: "sensors/humidity")

You can monitor this data with:

```bash
# Listen for all sensor data
mosquitto_sub -h your.mqtt.broker -t "sensors/#"
```

## Troubleshooting

### Common Issues

1. **Unable to access GPIO**: Make sure you're running with `sudo` or the proper permissions
   
   ```bash
   # For Docker
   docker run --device /dev/gpiomem:/dev/gpiomem rpi-mqtt-device
   
   # For direct run
   sudo python3 rpi_ky015_mqtt_publish.py
   ```

2. **Connection refused**: Check if the MQTT broker address and port are correct
   
   ```bash
   # Test connection to broker
   mosquitto_pub -h your.mqtt.broker -p 8080 -t test -m "test"
   ```

3. **DHT11 sensor not reading**: Ensure proper wiring and that you're using the correct GPIO pin

4. **WebSockets issues**: Try switching to TCP mode
   
   ```bash
   docker run -e USE_WEBSOCKETS=false rpi-mqtt-device
   ```

## License

This project is distributed under the MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.