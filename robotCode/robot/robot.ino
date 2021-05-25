//motor 1
int ln1 = 0; //D3
int ln2 = 4; //D2
int ena = 5; //D1

//motor 2
int ln3 = 14; //D5
int ln4 = 12; //D6
int enb = 13; //D7


void setup() 
{
  pinMode(ln1, OUTPUT);
  pinMode(ln2 , OUTPUT);
  pinMode(ena , OUTPUT);
 
  pinMode(ln3, OUTPUT);
  pinMode(ln4 , OUTPUT);
  pinMode(enb , OUTPUT);
  

}

void set_speed(int Speed)
{
 analogWrite(ena,Speed);
 analogWrite(enb,Speed);
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
  digitalWrite(ln1,LOW);
  digitalWrite(ln2 , HIGH);
  digitalWrite(ln3, HIGH);
  digitalWrite(ln4 , LOW); 
  }
  
void move_left(int Speed)
{
   set_speed(Speed);
  digitalWrite(ln1,HIGH);
  digitalWrite(ln2 , LOW);
  digitalWrite(ln3, LOW);
  digitalWrite(ln4 , HIGH); 
  }

void loop()
{
  // move forward , set speed to 255 out of possible range 0~255
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
