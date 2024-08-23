#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Home_ext";
const char* password = "9731300951";
const char* serverName = "http://192.168.0.114/log_memory";  // actual FASTAPI server URL

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {
  // Log memory usage
  logMemoryUsage();
  
  // Delay between measurements
  delay(1000);  // Log every 1 seconds
}

void logMemoryUsage() 
{
  int freeMemory = ESP.getFreeHeap();
  Serial.print("Free Memory: ");
  Serial.println(freeMemory);

  // Send data to the database
  // if (WiFi.status() == WL_CONNECTED) {
  //   WiFiClient client;
  //   HTTPClient http;

  //   String url = String(serverName) + "?free_memory=" + String(freeMemory);
  //   http.begin(client, url);
    
  //   int httpCode = http.GET();  // Send GET request
  //   if (httpCode > 0) {
  //     String payload = http.getString();
  //     Serial.println(payload);
  //   } else {
  //     Serial.println("Error in sending request");
  //   }
    
  //   http.end();
  // }
}
