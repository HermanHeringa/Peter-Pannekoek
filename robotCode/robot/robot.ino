//motor 1
int ln1 = 32;
int ln2 = 33;
int ena = 15;

//motor 2
int ln3 = 21;
int ln4 = 22;
int enb = 14;

const int freq = 5000;
const int pwmChannel_1 = 0;
const int pwmChannel_2 = 0;
const int resolution = 8;

void setup() 
{
  pinMode(ln1, OUTPUT);
  pinMode(ln2 , OUTPUT);
  pinMode(ena , OUTPUT);
 
  pinMode(ln3, OUTPUT);
  pinMode(ln4 , OUTPUT);
  pinMode(enb , OUTPUT);
  
  ledcSetup(pwmChannel_1, freq, resolution);
  ledcSetup(pwmChannel_2, freq, resolution);
  ledcAttachPin(ena, pwmChannel_1);
  ledcAttachPin(enb, pwmChannel_2);

}

void set_speed(int Speed)
{
  ledcWrite(pwmChannel_1, Speed);
  ledcWrite(pwmChannel_2, Speed);
 }
 
void move_forward(int Speed)
{ 
  set_speed(Speed);
  digitalWrite(ln1, LOW);
  digitalWrite(ln2 , HIGH);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , HIGH);
  }
  
void move_back(int Speed)
{
  set_speed(Speed);
  digitalWrite(ln1, HIGH);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, HIGH);
  digitalWrite(ln4 , LOW);
  }
  
void motor_off()
{
  digitalWrite(ln1,LOW);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , LOW); 
  }
  
void move_right(int Speed)
{
  set_speed(Speed);
  digitalWrite(ln1,HIGH);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , HIGH); 
  }
  
void move_left(int Speed)
{
  set_speed(Speed);
  digitalWrite(ln1,LOW);
  digitalWrite(ln2 , HIGH);
  digitalWrite(ln3, HIGH);
  digitalWrite(ln4 , LOW); 
  }


void loop()
{
  move_forward(255);
  delay(3000);
  motor_off();
  delay(3000);
  move_back(255);
  delay(3000);
  motor_off();
  delay(3000);
  move_right(255);
  delay(3000);
  motor_off();
  delay(3000);
   move_left(255);
  delay(3000);
  motor_off();
  delay(3000);
}
