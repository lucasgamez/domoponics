//#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>
/******************************************
* Change sensor ID HERE
* 
**/
const String humidity_sensor = "sensor_id=7";
const String temperature_sensor = "sensor_id=6";
const String lux_sensor = "sensor_id=8";

/******************************************
* PIN definition 
* 
**/
#define DHTPIN 12     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11 // DHT 11
#define LED_PIN 14    // Digital pin connected to the communication led
#define LUXPIN 16     // Analog led connected to the photoresistor

/******************************************
* Wifi/http setup 
* 
**/

WiFiClient wifiClient;
const char* ssid = "RollingPearl"; // Replace with your Wi-Fi network name
const char* password = "Rolling1nTheWorld"; // Replace with your Wi-Fi network password
const char* serverUrl = "http://192.0.0.112/sensors/"; // Replace with your Django server URL

DHT_Unified dht(DHTPIN, DHTTYPE);


/******************************************
* Setup function
* 
**/
void setup() {
  Serial.begin(9600);
  
  pinMode(LED_PIN, OUTPUT); // Set the LED pin as an output
  digitalWrite(LED_PIN, HIGH); // Turn on the LED


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    digitalWrite(LED_PIN, LOW); // Turn off the LED while connecting
    delay(250);
    digitalWrite(LED_PIN, HIGH); // Turn on the LED while waiting to connect
    delay(250);
  }
    //Connection succesful patern
    digitalWrite(LED_PIN, LOW); 
    delay(100);
    digitalWrite(LED_PIN, HIGH); 
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
    digitalWrite(LED_PIN, HIGH); 
    delay(100);
    digitalWrite(LED_PIN, LOW);

  dht.begin();
}

/******************************************
* Main loop 
* 
**/
void loop() {
  delay(2000); //Delay for sending data

  /******************/
  // Temperature and humidity
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  String temperature = "value=" + String(event.temperature);
  dht.humidity().getEvent(&event);
  String humidity = "value=" + String(event.relative_humidity);

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  //Get photo resistor value
  String photoResistorValue = "value=" + String(analogRead(LUXPIN));

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(wifiClient,serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCodeT = http.POST(humidity_sensor + "&" + humidity);
    int httpResponseCodeH = http.POST(temperature_sensor + "&" + temperature);
    int httpResponseCodeL = http.POST(lux_sensor + "&" + photoResistorValue);

    if (httpResponseCodeT > 0) {
      Serial.print("HTTP response code: ");
      Serial.println(httpResponseCodeT);
      digitalWrite(LED_PIN, HIGH); 
      delay(100);
      digitalWrite(LED_PIN, LOW);
    } else {
      Serial.println("Error sending data to server.");
    }

    http.end();
  } else {
    //If no connection, turn on the LED and wait to be rebooted
    Serial.println("WiFi connection lost.");
    digitalWrite(LED_PIN, HIGH); 
  }
}
