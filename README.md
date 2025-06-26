# Interaction between VR and the Real World

This project demonstrates an interactive system bridging Virtual Reality (VR) with physical IoT devices. Users within a VR environment can monitor sensor data and control actuators in the real world, facilitated by a backend server and MQTT communication.

## Project Components

The project is structured into three main components:

1.  **Frontend (Unity VR Application)**:
    -   Located in the `frontend/` directory.
    -   A Unity application providing the VR interface.
    -   Allows users to visualize sensor data (temperature, humidity) and send commands to control a light and a servo motor.
    -   Communicates with the backend via HTTP REST API calls.
    -   For more details, see `frontend/README.md`.

2.  **Backend (Flask Server)**:
    -   Located in the `backend/` directory.
    -   A Python Flask application that acts as a bridge between the VR frontend and the IoT device.
    -   Provides RESTful API endpoints for the frontend.
    -   Communicates with the IoT device(s) using the MQTT protocol.
    -   Stores sensor data in a database and provides historical data access.
    -   For more details, see `backend/README.md`.

3.  **Device (Raspberry Pi Client)**:
    -   Located in the `device/` directory.
    -   A Python script designed to run on a Raspberry Pi (or similar IoT device).
    -   Reads data from a DHT11 sensor (temperature and humidity).
    -   Controls an LED (light) and a servo motor based on commands received via MQTT.
    -   Publishes sensor data to MQTT topics.
    -   For more details, see `device/README.md`.

## System Architecture

```
┌───────────────────┐      HTTP REST API      ┌────────────────┐      MQTT      ┌────────────────┐
│                   │<---------------------->│                │<--------------->│                │
│  VR Frontend      │                         │ Backend Server │                 │  IoT Device    │
│ (Unity)           │---------------------->│ (Flask)        │-------------->│ (Raspberry Pi) │
│                   │      (Commands)         │                │   (Commands)  │                │
└───────────────────┘                         └────────────────┘                 └────────────────┘
        ^                                             │                                │
        │                                             │                                │
        │                                             ▼                                ▼
        └─────────────────────────────────────(Sensor Data)────────────────────────────┘
                                         (via MQTT then API)
```

## Features

-   **Real-time Monitoring**: View live temperature and humidity data from the IoT device in VR.
-   **Remote Control**:
    -   Turn a light (LED) on or off.
    -   Control a servo motor's direction and angle.
-   **Data Persistence**: Sensor data is stored by the backend, allowing for historical data retrieval.
-   **MQTT Communication**: Robust and lightweight messaging protocol for device communication.
-   **Dockerized Components**: The backend and device applications are containerized with Docker for ease of deployment and scalability.

## General Setup

To get the entire system running, you'll need to set up each component.

### Prerequisites

-   Git
-   Docker and Docker Compose (for backend and device)
-   Unity Hub and Unity Editor (for frontend)
-   Python 3.11+ (if running backend or device scripts directly)
-   An MQTT Broker (e.g., Mosquitto). The backend `docker-compose.yml` includes a Mosquitto service.

### Installation & Running

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/Incteraction-between-VR-and-the-real-world.git
    cd Incteraction-between-VR-and-the-real-world
    ```

2.  **Setup the Backend:**
    -   Navigate to the `backend/` directory.
    -   Follow the instructions in `backend/README.md` (either Docker or local Python setup).
    -   Ensure the backend server is running and the MQTT broker is accessible. The default `docker-compose up -d` in the backend directory will also start a Mosquitto MQTT broker.

3.  **Setup the Device:**
    -   Navigate to the `device/` directory.
    -   Follow the instructions in `device/README.md` for hardware setup and running the script (either Docker or direct Python execution).
    -   Configure the device script to connect to the MQTT broker used by the backend. If using the backend's Docker Compose setup, the broker address will be `mosquitto` (container name) or the host's IP if the device is external to the Docker network.

4.  **Setup the Frontend:**
    -   Navigate to the `frontend/` directory.
    -   Follow the instructions in `frontend/README.md` to open and run the Unity project.
    -   Ensure the Unity application is configured to communicate with the running backend server's API endpoints (e.g., `http://localhost:5000/api/mqtt` if running backend locally, or the appropriate IP if backend is on a different machine/container).

## Configuration Overview

-   **Backend (`backend/.env` or environment variables):**
    -   `BROKER_ADDRESS`: MQTT broker address (e.g., `mosquitto` if using backend's docker-compose, or `localhost` if running broker locally).
    -   `BROKER_PORT`: MQTT broker port (e.g., `9001` for WebSockets, `1883` for standard MQTT).
    -   `DATABASE_URI`: Connection string for the database.
-   **Device (environment variables or in script):**
    -   `BROKER_ADDRESS`, `BROKER_PORT`: MQTT broker details.
    -   GPIO pin configurations for sensors and actuators.
-   **Frontend (Unity Scripts):**
    -   API base URL for the backend server. This needs to be set in the relevant C# scripts that make HTTP calls.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3.  **Make your changes.**
4.  **Commit your changes** with a clear and descriptive commit message:
    ```bash
    git commit -m "feat: Implement new feature X"
    ```
    (Consider using [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.)
5.  **Push your changes** to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```
6.  **Open a Pull Request** against the main repository.

Please ensure your code adheres to any existing coding styles and include tests if applicable.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details (if one exists, otherwise assume MIT or specify).
```
