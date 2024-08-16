#include <Wire.h>
#include <MPU6050.h>
#include <WiFi.h>
#include <WebSocketsClient.h>

// WiFi credentials
const char* ssid = "pookies";
const char* password = "vQ$O(lxtlv3f";

// WebSocket server details
const char* websockets_server = "ws://157.28.2.27/ws";
const uint16_t websockets_port = 5000; // Replace with your server's port if different

MPU6050 mpu;
WebSocketsClient webSocket;

void setup() {
    Serial.begin(115200);

    // Initialize MPU6050
    Wire.begin();
    mpu.initialize();
    if (!mpu.testConnection()) {
        Serial.println("MPU6050 connection failed");
        while (1);
    }

    // Connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Connect to WebSocket server
    webSocket.begin(websockets_server, websockets_port, "/");
    webSocket.onEvent(webSocketEvent);
}

void loop() {
    webSocket.loop();

    // Read acceleration values
    int16_t ax, ay, az;
    mpu.getAcceleration(&ax, &ay, &az);

    // Calculate magnitude
    float magnitude = sqrt(ax * ax + ay * ay + az * az) / 16384.0; // Convert to 'g' units
    Serial.print("Magnitude: ");
    Serial.println(magnitude);

    // Send magnitude to WebSocket server
    String magnitudeStr = String(magnitude, 2);
    webSocket.sendTXT(magnitudeStr);

    delay(500); // Send data every 1 second
}

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
    switch(type) {
        case WStype_DISCONNECTED:
            Serial.println("WebSocket Disconnected");
            break;
        case WStype_CONNECTED:
            Serial.println("WebSocket Connected");
            break;
        case WStype_TEXT:
            Serial.printf("WebSocket Received Text: %s\n", payload);
            break;
    }
}