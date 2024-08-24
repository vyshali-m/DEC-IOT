#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

ESP8266WebServer server(80);  // Create a web server on port 80

#define MAX_ENTRIES 1  // Adjust this based on your memory constraints

const char* ssid = "Home_ext";
const char* password = "9731300951";
const unsigned long TIMEOUT_MS = 2000;  // Set timeout to 2000 milliseconds (2 seconds)

// FastAPI server details
const char* serverName = "http://thoroughly-correct-rooster.ngrok-free.app/endpoint";  // Replace with your FastAPI server URL

WiFiClient wifiClient;

// Structure to hold the parameters
struct Parameters {
  unsigned long timestamp;
  int memoryUsage;
  int networkTrafficVolume;
  int packetSize;
  int responseTime;
  float errorRate;
  float powerConsumption;
};

Parameters dataLog[MAX_ENTRIES];
int logIndex = 0;

unsigned long lastMillis = 0;
int requestCount = 0;
int failedRequests = 0;

// Counters for network traffic tracking
unsigned long bytesSent = 0;
unsigned long bytesReceived = 0;

// Function to collect parameters
int getMemoryUsage() {
  return ESP.getFreeHeap();
}

// int getNetworkTrafficVolume() {
//   return WiFi.RSSI();
// }

unsigned long getNetworkTrafficVolume() {
  return bytesSent + bytesReceived;
}

int getPacketSize() {
  if (server.client().available()) {
    return server.client().available();
  }
  return 0;
}

int getResponseTime() {
  unsigned long startTime = millis();
  // Simulate a request to self to measure response time
  if (!server.client().connected()) {
   return -1;
  }
  unsigned long endTime = millis();
  return endTime - startTime;
}

float getErrorRate() {
  return (requestCount == 0) ? 0 : (float)failedRequests / requestCount;
}

float getPowerConsumption() {
  int adcValue = analogRead(A0);
  float voltage = adcValue * (3.3 / 1024.0);
  float current = voltage / 0.185;
  return current;
}


// Function to send data and track the number of bytes sent and received
// void sendData(const String& jsonData) {
//   HTTPClient http;
//   http.begin(wifiClient, serverName);
//   http.addHeader("Content-Type", "application/json");

//   // Track bytes sent
//   bytesSent += jsonData.length();

//   int httpResponseCode = http.POST(jsonData);  // Send the data

//   if (httpResponseCode > 0) {
//     String response = http.getString();
//     bytesReceived += response.length();  // Track bytes received
//     Serial.println(jsonData);
//     Serial.println("Data sent successfully");
//     Serial.println(response);
//   } else {
//     Serial.print("Error sending data: ");
//     Serial.println(httpResponseCode);
//     failedRequests++;  // Track failed requests
//   }

//   http.end();
// }

// Function to reset network traffic counters
void resetTrafficCounters() {
  bytesSent = 0;
  bytesReceived = 0;
}

// Log parameters every second
void logParameters() 
{
  if (logIndex < MAX_ENTRIES) {
    dataLog[logIndex].timestamp = millis();
    dataLog[logIndex].memoryUsage = getMemoryUsage();
    dataLog[logIndex].networkTrafficVolume = getNetworkTrafficVolume();
    dataLog[logIndex].packetSize = getPacketSize();
    dataLog[logIndex].responseTime = getResponseTime();
    dataLog[logIndex].errorRate = getErrorRate();
    dataLog[logIndex].powerConsumption = getPowerConsumption();
    logIndex++;
  }

  // Check if the MAX_ENTRIES limit has been reached
  if (logIndex >= MAX_ENTRIES) {
    // Prepare the data in JSON format
    String jsonData = "{ \"batch data\" : [";
    for (int i = 0; i < MAX_ENTRIES; i++) {
      jsonData += "{";
      jsonData += "\"timestamp\": " + String(dataLog[i].timestamp) + ",";
      jsonData += "\"freeHeapMemory\": " + String(dataLog[i].memoryUsage) + ",";
      jsonData += "\"networkTrafficVolume\": " + String(dataLog[i].networkTrafficVolume) + ",";
      jsonData += "\"packetSize\": " + String(dataLog[i].packetSize) + ",";
      jsonData += "\"responseTime\": " + String(dataLog[i].responseTime) + ",";
      jsonData += "\"errorRate\": " + String(dataLog[i].errorRate) + ",";
      jsonData += "\"powerConsumption\": " + String(dataLog[i].powerConsumption);
      jsonData += "}";
      if (i < MAX_ENTRIES - 1) {
        jsonData += ",";
      }
    }
    jsonData += "]}";

    // Send data to FastAPI server
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      http.begin(wifiClient, serverName);  // Updated API usage
      http.addHeader("Content-Type", "application/json");

      // Track bytes sent
      bytesSent += jsonData.length();
      int httpResponseCode = http.POST(jsonData); //jsonData

      Serial.println(httpResponseCode);
      Serial.println("Server Name:");
      Serial.println(serverName);

      if (httpResponseCode > 0) {
        String response = http.getString();  // Get the response payload
        Serial.println(jsonData);
        Serial.println("Data sent successfully");
        Serial.println(response);
      } else {
        Serial.print("Error sending data: ");
        Serial.println(httpResponseCode);

      }

      http.end();
    } else {
      Serial.println("Error in WiFi connection");
    }

    // Reset logIndex after sending the data
    logIndex = 0;

    // Reset traffic counters after logging the data
    resetTrafficCounters();
  }
}



// Handle incoming HTTP request and respond
void handleRoot() {
  Serial.println("Received a request");
  requestCount++;

  unsigned long startTime = millis();  // Start the timer
  // Simulate request processing
  String response = "Hello from IOT-device-1";
  bytesSent += response.length();
  server.send(200, "text/plain", response);
  unsigned long endTime = millis();  // End the timer
  
  if (endTime - startTime > TIMEOUT_MS) 
  {
    Serial.println("Request timed out.");
    failedRequests++;  // Increment failed requests on timeout
  }
}

void handleNotFound() 
{
  String response = "404: Not Found";
  bytesSent += response.length();
  server.send(404, "text/plain", response);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Print the device IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Define the route for the root URL
  server.on("/", handleRoot);

  // Define the response for any undefined routes
  server.onNotFound(handleNotFound);

  // Start the server
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();  // Handle incoming client requests

  // Log parameters every 1 second
  if (millis() - lastMillis >= 1000) {
    lastMillis = millis();
    logParameters();
  }
}
