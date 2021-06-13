#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <HMC5883L.h>
HMC5883L compass;

#define HOST_SSID "AndroidAP"
#define HOST_PASS "pleo9996"
#define UDP_PORT 4210
IPAddress HOST_IP =IPAddress(224, 0, 1, 3);

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


void setup() 
{
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
  while (WiFi.status() != WL_CONNECTED)
  {
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
  while (!compass.begin())
  {
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
  compass.setOffset(128, -158);

  
  }

//main loop
void loop()
{
   delay(5000);
  rotate(180);
  delay(2000);
  move_forward(200);
  delay(4000);
  rotate(90);
  move_forward(200);
  delay(2500);
  rotate(90);
  delay(1500);
   move_forward(200);
  delay(2500);
  rotate(90);
  delay(2500);
  move_forward(200);
  delay(5000);
  rotate(270);
  delay(4000);
  move_forward(200);
  delay(3000);
  motor_off();
    
 //commandFromCU();

}

void rotate( int angle){

    current_angle = getAngle();
    int target_angle = current_angle + angle;
    
    if (target_angle > 360){
      target_angle = target_angle % 360;
    }
   
    while(getAngle() != target_angle){
      move_right(170);
      delay(50);
    }
      motor_off();
}

//get current angle
int getAngle(){
 Vector norm = compass.readNormalize();

  // Calculate heading
  float heading = atan2(norm.YAxis, norm.XAxis);

  // Set declination angle on your location and fix heading
  // You can find your declination on: http://magnetic-declination.com/
  // (+) Positive or (-) for negative
  // For Bytom / Poland declination angle is 4'26E (positive)
  // Formula: (deg + (min / 60.0)) / (180 / M_PI);
  float declinationAngle = (1.0 + (49.0 / 60.0)) / (180 / M_PI);//rotterdam
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
  float headingDegrees = heading * 180/M_PI; 
  headingDegrees = (360 + (int)headingDegrees - 95) % 360;

  return headingDegrees;
}

//receive commands from Central Unit
void commandFromCU(){
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

//to send packet to Central unit
void sendPacket(String packet){
    String string= packet;
    char msg[255];
    string.toCharArray(msg,255);//convert string to char array
    UDP.beginPacketMulticast(HOST_IP, UDP_PORT, WiFi.localIP());
    UDP.write(msg);
    UDP.endPacket();
}

// set motor speed range 200-255
void set_speed(int Speed) {
  analogWrite(motorOneSpeed,Speed);
  analogWrite(motorTwoSpeed,Speed);
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
  digitalWrite(motorOneReverse,LOW);
  digitalWrite(motorOneForward , HIGH);
  digitalWrite(motorTwoReverse, HIGH);
  digitalWrite(motorTwoForward , LOW); 
}

//rotate left
void move_left(int speed) {
  set_speed(speed);
  digitalWrite(motorOneReverse,HIGH);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , HIGH); 
}

//don't move
void motor_off() {
  digitalWrite(motorOneReverse,LOW);
  digitalWrite(motorOneForward , LOW);
  digitalWrite(motorTwoReverse, LOW);
  digitalWrite(motorTwoForward , LOW); 
}
