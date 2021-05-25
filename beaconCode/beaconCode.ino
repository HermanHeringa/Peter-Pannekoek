#include <ESP8266WiFi.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);
  WiFi.begin("testtest", "88888888");

  Serial.print("\nConnecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
   int n = WiFi.scanNetworks();
  for (int i = 0; i < n; i++)
  {
    if (strstr(WiFi.SSID(i).c_str(), "ESP-")) {
      Serial.printf("%s (%ddBm)\n", WiFi.SSID(i).c_str(), WiFi.RSSI(i));
    }
  }
} 
