#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <HMC5883L.h>
HMC5883L compass;

#define HOST_SSID "Bezems"
#define HOST_PASS "aaaaaaaa"
#define UDP_PORT 1337
IPAddress HOST_IP = IPAddress(192, 168, 137, 1);

#define MOTOR_SPEED 180
#define ACCEPTABLE_ERROR 5

String STOP_MESSAGE = "stop";
String HEAD_MESSAGE = "head";

String incomingMessage = "";
bool wahedWaar = false;
bool wahedWaar2 = false;
int target_heading = 0;
int dest_heading = 0;
int angle_error = 0;
int magnetic_offset = 0;

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
int current_angle = 0;

void setup() {
  //setup motors
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
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());


  // Setup UDP
  UDP.begin(UDP_PORT);
  Serial.print("Listening on UDP port ");
  Serial.println(UDP_PORT);

  // Initialize Initialize HMC5883L
  Serial.println("Initialize HMC5883L");
  while (!compass.begin()) {
    Serial.println("Could not find a valid HMC5883L sensor, check wiring!");
    delay(500);
  }

  // Set measurement range
  compass.setRange(HMC5883L_RANGE_1_3GA);

  // Set measurement mode
  compass.setMeasurementMode(HMC5883L_CONTINOUS);

  // Set data rate
  compass.setDataRate(HMC5883L_DATARATE_30HZ);

  // Set number of samples averaged
  compass.setSamples(HMC5883L_SAMPLES_8);

  // Set calibration offset. See HMC5883L_calibration.ino
  compass.setOffset(75, -89);//67:-182

  magnetic_offset = getAngle();

  sendPacket("wake#red");
}

//main loop
void loop() {

  incomingMessage = commandFromCU();
  if (incomingMessage != "") {

    if (incomingMessage == STOP_MESSAGE) {
      //Stop driving
      motor_off();
      wahedWaar2 = false;
      Serial.println("STOP");
    }
    else if (incomingMessage.substring(0, 4) == HEAD_MESSAGE) {
      String data = incomingMessage.substring(5);
      target_heading = data.toInt();
      wahedWaar = true;
      wahedWaar2 = true;
      Serial.println(data);
    }
    incomingMessage = "";
  }

  if (wahedWaar2) {
    if (wahedWaar) {

      if (target_heading > 180.0) {
        target_heading = 360 - target_heading;
      }
      dest_heading = - target_heading;  // flip angle to clockwise

      if (dest_heading < 0) {
        dest_heading = 360 + dest_heading;
      }

      
      wahedWaar = false;
    }

    current_angle = getAngle();
    angle_error = ((dest_heading - current_angle + 360) % 360);


    if (angle_error > 180 && angle_error < 360 - ACCEPTABLE_ERROR) {
      //turn left
      Serial.println("LEFT");
      move_left(MOTOR_SPEED);

    } else if (angle_error < 180 && angle_error > ACCEPTABLE_ERROR) {
      //turn right
      Serial.println("RIGHT");
      move_right(MOTOR_SPEED);

    }
    if ((angle_error > (360 - ACCEPTABLE_ERROR)) || (angle_error < ACCEPTABLE_ERROR)) {
      //forward
      Serial.println("FORWARD");
      
      move_forward(MOTOR_SPEED);
    }
  }
  sendPacket(String(getAngle()));

  /*
  Serial.print("target heading: ");
  Serial.println(target_heading);
  
  Serial.print("current heading: ");
  Serial.println(current_angle);
  
  Serial.print("destination heading: ");
  Serial.println(dest_heading);
  
  Serial.print("angle error: ");
  Serial.println(angle_error);
  Serial.println("=================================");

  delay(500); */
  
  yield();
}

//get current angle
int getAngle() {
  Vector norm = compass.readNormalize();

  // Calculate heading
  float heading = atan2(norm.YAxis, norm.XAxis);

  // Set declination angle on your location and fix heading
  // You can find your declination on: http://magnetic-declination.com/
  // (+) Positive or (-) for negative
  // For Bytom / Poland declination angle is 4'26E (positive)
  // Formula: (deg + (min / 60.0)) / (180 / M_PI);
  float declinationAngle = (1.0 + (49.0 / 60.0)) / (180.0 / M_PI);//rotterdam
  heading += declinationAngle;

  // Correct for heading < 0deg and heading > 360deg
  if (heading < 0)
  {
    heading += 2 * PI;
  }

  if (heading > 2 * PI)
  {
    heading -= 2 * PI;
  }

  // Convert to degrees
  float headingDegrees = heading * 180 / M_PI;
  headingDegrees = (360 + (int)headingDegrees - 95) % 360;

  return ((((int)headingDegrees - magnetic_offset) + 360) % 360);
}

//receive commands from Central Unit
String commandFromCU() {
  int packetSize = UDP.parsePacket();
  if (packetSize) {
    //Serial.print("Received packet! Size: ");
    //Serial.println(packetSize);
    int len = UDP.read(packet, 255);
    if (len > 0)
    {
      packet[len] = '\0';
    }
    Serial.print("Packet received: ");
    Serial.println(packet);
    String mystring(packet);
    return mystring;
  } else {
    return "";
  }
}


//to send packet to Central unit
void sendPacket(String packet) {
  Serial.println(packet);
  String string = packet;
  char msg[255];
  string.toCharArray(msg, 255); //convert string to char array
  UDP.beginPacket(HOST_IP, UDP_PORT);
  UDP.write(msg);
  UDP.endPacket();
}

// set motor speed range 200-255
void set_speed(int Speed) {
  analogWrite(motorOneSpeed, Speed);
  analogWrite(motorTwoSpeed, Speed);
}

//move forward
void move_forward(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH);
}

//move back
void move_back(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse, HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW);
}

//rotate right
void move_right(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW);
}

//rotate left
void move_left(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse, HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH);
}

//don't move
void motor_off() {
  digitalWrite(motorOneReverse, LOW);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , LOW);
}
