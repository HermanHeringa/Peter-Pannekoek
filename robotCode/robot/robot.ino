#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define HOST_SSID "testtest"
#define HOST_PASS "88888888"
#define MY_SSID "ESP-14"
#define MY_PASS "2xjYrA2Ny3VwyJuh"
#define UDP_PORT 4210

//motor 1
int ln1 = 0; //D3
int ln2 = 4; //D2
int ena = 5; //D1

//motor 2
int ln3 = 14; //D5
int ln4 = 12; //D6
int enb = 13; //D7

WiFiUDP UDP;
char packet[255];
char reply[] = "Packet received!";

void setup() 
{
  pinMode(ln1, OUTPUT);
  pinMode(ln2 , OUTPUT);
  pinMode(ena , OUTPUT);
 
  pinMode(ln3, OUTPUT);
  pinMode(ln4 , OUTPUT);
  pinMode(enb , OUTPUT);
  
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

void loop()
{
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
}

//Packets zijn een direction (1 tot 3 cijfers), gevolgd door een plat streepje (-), gevolgd door een snelheid (1 tot 3 cijfers), met daarna een terminating zero.
void packetHandler (char input[255]) {
  int temp;
  char direction[3];
  for (int i = 0; input[i] != '-'; i++) {
    direction[i] = input[i];
    temp = i;
  }
  direction[temp+1] = '\0';
  char speed[3];
  for (int i = 0; input[i+temp+1] != '\0'; i++) {
    speed[i] = input[i+temp];
  }
  speed[i+1] = '\0';
  temp = 0;
  int realDirection = atoi(direction);
  int realSpeed = atoi(speed);
  if (realDirection != 0) {
    turn(realDirection);
  }
  set_speed(realSpeed);
  move_forward();
}

void turn(int direction) {
  set_speed(255);
  if (direction > 180) {
    move_left();
  }
  else {
    move_right();
  }
   while(getAngle() != direction) {
    //aan het draaien, verwijder deze code als magnetometer code toegevoegd is
    delay(300);
    break;
   }
   motor_off();
}

int getAngle() {
  //TODO: magnetometer code
  return 0;
}

void set_speed(int Speed) {
  analogWrite(ena,Speed);
  analogWrite(enb,Speed);
}
 
void move_forward() { 
  digitalWrite(ln1, LOW);
  digitalWrite(ln2 , HIGH);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , HIGH);
}
  
void move_back() {
  digitalWrite(ln1, HIGH);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, HIGH);
  digitalWrite(ln4 , LOW);
}
  
void motor_off() {
  digitalWrite(ln1,LOW);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , LOW); 
}
  
void move_right() {
  digitalWrite(ln1,LOW);
  digitalWrite(ln2 , HIGH);
  digitalWrite(ln3, HIGH);
  digitalWrite(ln4 , LOW); 
}
  
void move_left() {
  digitalWrite(ln1,HIGH);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , HIGH); 
}
