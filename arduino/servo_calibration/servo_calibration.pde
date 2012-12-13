#include <Servo.h> 

int SERVO_PIN = 4;
int START_POS = 15;
int END_POS = 40;

int position = START_POS;

Servo servo;

void setup() {
  Serial.begin(9600);
  Serial.println("Starting..."); 
  
  servo.attach(SERVO_PIN);
  servo.write(position);
}

void loop(){
  position++;
  servo.write(position);
  Serial.println(position); 
  delay(1000);
  
  if(position == END_POS){
    servo.write(START_POS+(END_POS-START_POS)/2);
    while(1);
  }
}
