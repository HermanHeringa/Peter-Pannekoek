#include <ESP8266WiFi.h>

String hostSSID = "testtest";
String hostPass = "88888888";
String mySSID = "ESP-0";
String myPass = "2xjYrA2Ny3VwyJuh";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  WiFi.begin(hostSSID, hostPass);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  boolean fakeNetwork = WiFi.softAP(mySSID, MyPass);
  if (fakeNetwork) {
    Serial.println("Network created.");
  }
  else {
    Serial.println("Network creation failed");
  }
}

void loop() {
} 
