#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

#define HOST_SSID "testtest"
#define HOST_PASS "88888888"
#define MY_SSID "ESP0-4"
#define MY_PASS "2xjYrA2Ny3VwyJuh"
#define UDP_PORT 4210

//magnetometer
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);

//motor 1
int motorOneReverse = 0; //D3
int motorOneForward = 12; //D6
int motorOneSpeed = 13; //D7

//motor 2
int motorTwoReverse = 14; //D5
int motorTwoForward = 12; //D6
int motorTwoSpeed = 13; //D7

WiFiUDP UDP;
char packet[255];
char reply[] = "Packet received!";

void setup()
{
  pinMode(motorOneReverse, OUTPUT);
  pinMode(motorOneForward , OUTPUT);
  pinMode(motorOneSpeed , OUTPUT);

  pinMode(motorTwoReverse, OUTPUT);
  pinMode(motorTwoForward , OUTPUT);
  pinMode(motorTwoSpeed , OUTPUT);

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

  // Setup magnetometer
  if (!mag.begin())
  {
    /* There was a problem detecting the HMC5883 ... check your connections */
    Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
    while (1);
  }
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
    /*String stringPacket(packet);
      set_speed(255);
      if (stringPacket == "f")
      {
      move_forward();
      Serial.println("forward");
      }
      else if (stringPacket == "b")
      {
      move_back();
      Serial.println("back");
      }
      else if (stringPacket == "r")
      {
      move_right();
      Serial.println("right");
      }
      else if (stringPacket == "l")
      {
      Serial.println("left");
      move_left();
      }
      else if (stringPacket == "s")
      {
      Serial.println("stop");
      motor_off();
      }*/
    packetHandler(packet);
  }
}

//Packets zijn een relatieve direction (1 tot 3 cijfers), gevolgd door een plat streepje (-), gevolgd door een snelheid (1 tot 3 cijfers), met daarna een terminating zero.
void packetHandler (char input[255]) {
  int temp;
  int i;
  char direction[4];
  for (i = 0; input[i] != '-'; i++) {
    direction[i] = input[i];
    temp = i + 1;
  }
  direction[temp] = '\0';
  Serial.print("Direction: ");
  Serial.println(direction);
  char speed[4];
  for (i = 0; input[i + temp + 1] != '\0'; i++) {
    speed[i] = input[i + temp + 1];
  }
  speed[i] = '\0';
  Serial.print("Speed: ");
  Serial.println(speed);
  temp = 0;
  int iDirection = atoi(direction);
  int iSpeed = atoi(speed);
  if (iDirection != 0) {
    turn(iDirection);
  }
  set_speed(iSpeed);
  move_forward();
}

void turn(int direction) {
  int startAngle = getAngle();
  int currentAngle = startAngle;
  set_speed(255);
  while (currentAngle != ((startAngle + direction) % 360)) {
    Serial.print("current angle: ");
    Serial.println(currentAngle);
    Serial.print("target angle: ");
    Serial.println((startAngle + direction) % 360);
    if (currentAngle > ((currentAngle + direction) % 360)) {
      move_left();
    }
    else {
      move_right();
    }
    currentAngle = getAngle();
  }
  motor_off();
}

int getAngle() {
  sensors_event_t event;
  mag.getEvent(&event);
  float heading = atan2(event.magnetic.y, event.magnetic.x);
  if (heading < 0) {
    heading += 2 * PI;
  }
  if (heading > 2 * PI) {
    heading -= 2 * PI;
  }
  float headingDegrees = heading * 180 / M_PI;
  return round(headingDegrees);
}

void set_speed(int Speed) {
  analogWrite(motorOneSpeed, Speed);
  analogWrite(motorTwoSpeed, Speed);
}

void move_forward() {
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH);
}

void move_back() {
  digitalWrite(motorOneReverse, HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW);
}

void motor_off() {
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , LOW);
}

void move_right() {
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW);
}

void move_left() {
  digitalWrite(motorOneReverse, HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH);
}
