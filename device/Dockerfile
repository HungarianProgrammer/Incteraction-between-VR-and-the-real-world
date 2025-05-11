FROM python:3.9-slim


RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY rpi_ky015_mqtt_publish.py .

# Set environment variables with the exact specified values
ENV BROKER_ADDRESS="" \
    BROKER_PORT=8080 \
    USE_WEBSOCKETS=true \
    TEMP_TOPIC="sensors/temperature" \
    HUMIDITY_TOPIC="sensors/humidity" \
    CONTROL_TOPIC="light" \
    MOTION_TOPIC="motion" \
    DHT_PIN=17 \
    LIGHT_GPIO_PIN=27 \
    SERVO_PIN=24 \
    READ_INTERVAL=2

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]