#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define HOST_SSID "testtest";
#define HOST_PASS "88888888";
#define MY_SSID "ESP-0";
#define MY_PASS "2xjYrA2Ny3VwyJuh";
#define UDP_PORT 4210
#define HOST_IP "192.168.137.1"

WiFiUDP UDP;
char packet[255];
char reply[] = "Packet received!";

void setup() {
  // Connect to host wifi network
  Serial.begin(9600);
  WiFi.begin(HOST_SSID, HOST_PASS);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  // Setup network for beacons to track
  boolean fakeNetwork = WiFi.softAP(MY_SSID, MY_PASS);
  if (fakeNetwork) {
    Serial.println("Network created.");
  }
  else {
    Serial.println("Network creation failed");
  }

  // Setup UDP
  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);
}

void loop() {
  int packetSize = UDP.parsePacket();
  if (packetSize) {
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize); 
    int len = UDP.read(packet, 255);
    if (len > 0)
    {
      packet[len] = '\0';
    }
    Serial.print("Packet received: ");
    Serial.println(packet);
  }

  // driving code here
} 
