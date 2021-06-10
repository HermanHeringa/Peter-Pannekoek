#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#define HOST_SSID "AndroidAP"
#define HOST_PASS "pleo9996"
#define MY_SSID "ESP-14"
#define MY_PASS "2xjYrA2Ny3VwyJuh"
#define UDP_PORT 4210
IPAddress HOST_IP =IPAddress(224, 0, 1, 3);


/* Assign a unique ID to this sensor at the same time */
Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);


//motor 1
int motorOneReverse = 0; //D3
int motorOneForward = 15; //D8
int motorOneSpeed = 2; //D4

//motor 2
int motorTwoReverse = 14; //D5
int motorTwoForward = 12; //D6
int motorTwoSpeed = 13; //D7

WiFiUDP UDP;
char packet[255];
char reply[] = "Packet received!";


void setup() 
{
  /* Initialise the sensor */
  if(!mag.begin())
  {
    /* There was a problem detecting the HMC5883 ... check your connections */
    Serial.println("Ooops, no HMC5883 detected ... Check your wiring!");
    while(1);
  }
  
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
}

void loop(void)
{

    getAngle();
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
    String mystring(packet);
    
    if(mystring=="f")
    {
      move_forward(180);
     
     Serial.println("forward");
     }
     else if(mystring=="b")
     {
      move_back(180);
      Serial.println("back");
      }
     else if(mystring=="r")
     {
      move_right(180);
     Serial.println("right");
      }
      else if(mystring=="l")
     {
      Serial.println("left");
      move_left(180);
      }
       else if(mystring=="s")
     {
      Serial.println("stop");
      motor_off();
      }
  }
}

void sendPacket(String packet){
    String string= packet;
    char msg[255];
    string.toCharArray(msg,255);
    UDP.beginPacketMulticast(HOST_IP, UDP_PORT, WiFi.localIP());
    UDP.write(msg);
    UDP.endPacket();
}


void getAngle(){
  /* Get a new sensor event */ 
  sensors_event_t event; 
  mag.getEvent(&event);

  float heading = atan2(event.magnetic.y, event.magnetic.x);
  float declinationAngle = 0.22;
  heading += declinationAngle;
 
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
 
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
 
  // Convert radians to degrees for readability.
  float headingDegrees = heading * 180/M_PI; 
  String HDegrees = String(headingDegrees);
  Serial.println(HDegrees);
  sendPacket(HDegrees);
 
  delay(100);
}

void set_speed(int Speed) {
  analogWrite(motorOneSpeed,Speed);
  analogWrite(motorTwoSpeed,Speed);
}
 
void move_forward(int speed) { 
  set_speed(speed);
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH);
}
  
void move_back(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse, HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW);
}
  
void motor_off() {
  digitalWrite(motorOneReverse,LOW);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , LOW); 
}
  
void move_right(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse,LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW); 
}
  
void move_left(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse,HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH); 
}
