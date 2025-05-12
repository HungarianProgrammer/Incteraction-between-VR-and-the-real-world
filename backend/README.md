# VR-IoT Integration Backend

This project provides a Flask backend that bridges Virtual Reality experiences with IoT devices using MQTT communication.

## Features

- RESTful API endpoints for controlling IoT devices and retrieving sensor data
- MQTT integration for real-time communication with IoT devices
- Supports temperature and humidity sensor data
- Light control functionality (on/off)
- Motion control with direction and angle settings
- Persistent database storage for temperature and humidity readings
- Historical data querying with time range filtering
- Statistics and aggregation of sensor data
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
- `DATABASE_URI`: Database connection string (default: sqlite:///iot_data.db)

## API Endpoints

### MQTT Status
- `GET /api/mqtt/status` - Check MQTT connection status

### Sensor Data
- `GET /api/mqtt/temperature` - Get the latest temperature reading
- `GET /api/mqtt/temperature/history` - Get historical temperature readings
- `GET /api/mqtt/humidity` - Get the latest humidity reading
- `GET /api/mqtt/humidity/history` - Get historical humidity readings
- `GET /api/mqtt/stats` - Get statistics about stored sensor data

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

## Database Schema

The application uses SQLAlchemy ORM with the following models:

### TemperatureData
- `id` (Integer, primary key)
- `value` (Float) - Temperature value in degrees Celsius
- `timestamp` (DateTime) - When the reading was taken

### HumidityData
- `id` (Integer, primary key)
- `value` (Float) - Humidity percentage value
- `timestamp` (DateTime) - When the reading was taken

## Historical Data Queries

The temperature and humidity history endpoints accept the following query parameters:

- `limit` (default: 100) - Maximum number of records to return
- `start_time` (optional) - Unix timestamp for the start of the time range
- `end_time` (optional) - Unix timestamp for the end of the time range

Example:
```
GET /api/mqtt/temperature/history?limit=50&start_time=1620000000&end_time=1620100000
```
