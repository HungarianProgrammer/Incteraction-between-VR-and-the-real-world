# VR-IoT Integration Backend

This project provides a Flask backend that bridges Virtual Reality experiences with IoT devices using MQTT communication.

## Features

- RESTful API endpoints for controlling IoT devices and retrieving sensor data
- MQTT integration for real-time communication with IoT devices
- Supports temperature and humidity sensor data
- Light control functionality (on/off)
- Motion control with direction and angle settings
- Containerized with Docker for easy deployment

## Setup and Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- MQTT broker (Mosquitto provided in the Docker setup)

### Local Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```

### Docker Deployment

1. Make sure Docker and Docker Compose are installed
2. Build and start the containers:
   ```
   docker-compose up -d
   ```

## Environment Variables

The application can be configured using the following environment variables:

- `BROKER_ADDRESS`: MQTT broker address (default: "mosquitto" for Docker, "localhost" for local)
- `BROKER_PORT`: MQTT broker port (default: 9001 for WebSockets)
- `USE_WEBSOCKETS`: Whether to use WebSockets for MQTT communication (default: true)
- `FLASK_ENV`: Application environment (development or production)

## API Endpoints

### MQTT Status
- `GET /api/mqtt/status` - Check MQTT connection status

### Sensor Data
- `GET /api/mqtt/temperature` - Get the latest temperature reading
- `GET /api/mqtt/humidity` - Get the latest humidity reading

### Device Control
- `GET /api/mqtt/light` - Get the current light status
- `POST /api/mqtt/light` - Control light state (on/off)
- `GET /api/mqtt/motion` - Get the current motion settings
- `POST /api/mqtt/motion` - Control motion (direction and angle)

### Testing
- `POST /api/mqtt/publish` - Publish test data to MQTT topics (for debugging)

## MQTT Topics

- `sensors/temperature` - Temperature sensor data
- `sensors/humidity` - Humidity sensor data
- `light` - Light control commands
- `motion` - Motion control commands
