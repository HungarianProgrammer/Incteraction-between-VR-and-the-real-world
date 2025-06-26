# Frontend - Unity VR Interface

This directory contains the Unity project for the VR interface that interacts with the IoT devices through the backend API.

## Project Overview

The Unity application provides a virtual reality environment where users can:

- View real-time sensor data (temperature and humidity) from the connected IoT device.
- Control a light connected to the IoT device (turn on/off).
- Control a servo motor connected to the IoT device (direction and angle).

The application communicates with the backend server, which in turn communicates with the IoT device via MQTT.

## Setup and Build

### Prerequisites

- Unity Hub
- Unity Editor (Version 2022.3.20f1 or compatible) - *Note: Check `frontend/IOTController/ProjectSettings/ProjectVersion.txt` for the exact version.*
- Git LFS (if not already installed, for handling large files if any are added in the future, though currently it seems not strictly necessary based on file listing)

### Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Incteraction-between-VR-and-the-real-world.git
    cd Incteraction-between-VR-and-the-real-world/frontend
    ```

2.  **Open the project in Unity Hub:**
    - Open Unity Hub.
    - Click on "Open" or "Add project from disk".
    - Navigate to the `frontend/IOTController` directory within the cloned repository and select it.
    - Unity Hub should automatically detect the correct Unity Editor version if it's installed. If not, it will prompt you to install it.

### Building the Application

1.  **Open the project in Unity Editor.**
2.  Go to `File > Build Settings...`.
3.  **Select your target platform** (e.g., Windows, Oculus, etc.).
4.  Ensure the scenes in `frontend/IOTController/Assets/Scenes/` are added to the "Scenes In Build". The main scene is likely `MainScene` or similar (you might need to confirm the exact main scene name).
5.  Click **"Switch Platform"** if you've changed the target platform.
6.  Click **"Build"** and choose a location to save the build.

    Alternatively, for development, you can click **"Build And Run"**.

## Running the Application

-   **In the Unity Editor:**
    1.  Open the main scene (e.g., `Assets/Scenes/SampleScene` or `MainScene` - please verify the correct scene name).
    2.  Press the "Play" button at the top of the editor.

-   **As a standalone build:**
    1.  Navigate to the directory where you built the application.
    2.  Run the executable file.

**Note:** Ensure the backend server is running and accessible by the Unity application for full functionality. The backend API endpoint is likely configured within one of the C# scripts in `Assets/Scripts` (e.g., a script responsible for API calls).

## Key Scripts

-   `Assets/DeviceController.cs`: Likely handles the logic for interacting with the backend API to send commands and receive data.
-   `Assets/IoTUIButton.cs`: May handle UI interactions for controlling devices.

(Please explore these scripts for more detailed understanding of the frontend logic.)

## Dependencies

The project uses standard Unity packages. Specific packages can be found in `frontend/IOTController/Packages/manifest.json`.
Key packages might include:
- Unity Input System
- TextMesh Pro
- Universal Render Pipeline (URP)

Check the `manifest.json` for a complete list.

## Configuration

- The backend server URL needs to be correctly configured within the Unity project. This is typically done in a C# script that makes HTTP requests. Look for a variable holding the base URL for the API (e.g., `http://localhost:5000/api/mqtt`).
- Ensure the MQTT broker settings on the backend are correct and that the backend can communicate with the device.
```
