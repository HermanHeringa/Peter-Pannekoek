#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define HOST_SSID "testtest"
#define HOST_PASS "88888888"
#define DRONE_ID "ESP-"
#define UDP_PORT 4210

WiFiUDP UDP;
char packet[255];
char reply[255];
char buff[5];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  delay(500);
  WiFi.begin(HOST_SSID, HOST_PASS);

  Serial.print("\nConnecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
}

void loop() {
  
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; i++)
  {
    if (strstr(WiFi.SSID(i).c_str(), DRONE_ID)) {
      strcpy(reply, WiFi.SSID(i).c_str());
      strcat(reply,  " (");
      strcat(reply, itoa(WiFi.RSSI(i), buff, 10));
      strcat(reply, "dBm)");
      UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
      UDP.write(reply);
      UDP.endPacket();
    }
  }
} 
