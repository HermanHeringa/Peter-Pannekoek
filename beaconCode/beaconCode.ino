#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define HOST_SSID "AndroidAP"
#define HOST_PASS "pleo9996"
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
  String astring= "hi";
  char msg[255];
  astring.toCharArray(msg,255);
  UDP.beginPacket(UDP.remoteIP(), UDP.remotePort());
  UDP.write(msg);
  UDP.endPacket();
} 
