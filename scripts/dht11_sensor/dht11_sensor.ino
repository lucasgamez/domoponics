#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define DHTPIN D4     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11 // DHT 11

const char* ssid = "your_SSID"; // Replace with your Wi-Fi network name
const char* password = "your_PASSWORD"; // Replace with your Wi-Fi network password
const char* serverUrl = "http://your_django_server_url.com/api/sensors/"; // Replace with your Django server URL

DHT_Unified dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  dht.begin();
}

void loop() {
  delay(2000);

  sensors_event_t event;
  dht.temperature().getEvent(&event);
  float temperature = event.temperature;
  dht.humidity().getEvent(&event);
  float humidity = event.relative_humidity;

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonBody = "{\"data_type\":\"temperature\", \"value\":\"" + String(temperature) + "\"}";
    int httpResponseCode = http.POST(jsonBody);

    if (httpResponseCode > 0) {
      Serial.print("HTTP response code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.println("Error sending data to server.");
    }

    http.end();
  } else {
    Serial.println("WiFi connection lost.");
  }
}
