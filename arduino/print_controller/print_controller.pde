#include <Servo.h> 

int FEED_PIN = 2;
int PAPER_PIN = 5;
int FRONT_SERVO_PIN = 4;
int BACK_SERVO_PIN = 6;
//int PRINT_PIN = 12;

int FEED_INT = 0;
int MOTOR_INT = 1;

int FEED_DELAY = 50; // Delay between the feed sensor trip and registering the paper feed
int OFF_DELAY = 20; // Milliseconds between pulses for the motor to be considered off
int END_FEED = 200; // Anything greater is considered ending the print job
int MAX_FEED_TIME = 1000; // Never allow a feed longer than this
int MIN_FEED_TIME = 50; // Minimum time paper must move to be considered fed

int SETUP_FEEDS = 3; // Number of feeds to ignore at the beginning of the print job

int START_PULSES = 15; // Number of pulses received before registering a motor start
int MIN_MOTOR_TIME = 10; // Minimum running time considered valid start/stop

int ON_FRONT_SERVO = 40;
int OFF_FRONT_SERVO = 18;
int ON_BACK_SERVO = 72;
int OFF_BACK_SERVO = 108;

unsigned long feed_time = -1;
int feed_count = 0;

boolean feed_state = false;
boolean print_state = false;
boolean ready_state = false;

unsigned long motorStart = -1;
unsigned long motorStop = -1;
unsigned long lastMotor = -1; 
double currSpeed = -1;

unsigned long encoderPulses = 0;

Servo frontServo;
Servo backServo;

void setup() {
  // put your setup code here, to run once:
  pinMode(FEED_PIN, INPUT);
  pinMode(PAPER_PIN, INPUT);
  //pinMode(PRINT_PIN, INPUT);

  attachInterrupt(MOTOR_INT, trackMotor, CHANGE);
  
  frontServo.attach(FRONT_SERVO_PIN);
  frontServo.write(OFF_FRONT_SERVO);
  backServo.attach(BACK_SERVO_PIN);
  backServo.write(OFF_BACK_SERVO);
  
  Serial.begin(9600);
  Serial.println("Ready to print"); 
}

// State 0: Print disabled
// State 1: Print ready
// State 2: Paper fed

void loop() {
  while(Serial.available() > 1)
    Serial.read();
  int incoming = Serial.read();
  if (incoming != -1)
    Serial.println(incoming);
  
  unsigned long time = millis();
  
  if(incoming == 1 || incoming == 49){
    // Enable printing
    if(!ready_state){
      attachInterrupt(FEED_INT,simulateFeed,FALLING);
      ready_state = true;
      Serial.println("Print enabled");
    }
  } else if ((incoming == 0 || incoming == 48) && ready_state){
    // Disable printing  
    stopPrintFeed();
    ready_state = false;
    detachInterrupt(FEED_INT);
    Serial.println("Print disabled");
  }
  
  if (ready_state && feed_time != -1 && time > feed_time){
    if(feed_state){
      Serial.println("Something went wrong");
      stopPrintFeed();
    } else {
      feed_state = true;
      pinMode(PAPER_PIN, OUTPUT);
      digitalWrite(PAPER_PIN,LOW);
      Serial.println("Paper fed");
    }
    feed_time = -1;
  } 
  
  if (motorStart != -1){
    if (lastMotor < (time-OFF_DELAY)){
      motorStop = lastMotor;
      int runTime = motorStop-motorStart;
      motorStart = -1;
      if(runTime > MIN_MOTOR_TIME){
        Serial.print("Motor stop, ran for: ");
        Serial.println(runTime);
        onMotorStop(runTime);
      }
    } else if(print_state && (
              time > (motorStart + MAX_FEED_TIME) 
              || ((time > (motorStart + END_FEED)) && (feed_count > SETUP_FEEDS))
              )) {
      stopPrintFeed();
    }
  }
}

void stopPrintFeed(){
  frontServo.write(OFF_FRONT_SERVO);
  backServo.write(OFF_BACK_SERVO);
  pinMode(PAPER_PIN, INPUT);
  detachInterrupt(FEED_INT);
}

void onMotorStop(int runTime){
  // Motor 
    if(print_state)
      feed_count += 1;
    if (feed_state && runTime > MIN_FEED_TIME && !print_state){
      print_state = true;
      Serial.println("Printing started");
      frontServo.write(ON_FRONT_SERVO);
      backServo.write(ON_BACK_SERVO);
      feed_count = 0;
    }
}



void simulateFeed(){
  feed_time = millis() + FEED_DELAY;
}

void trackMotor(){
  long time = millis();
  
  if (lastMotor < (time-OFF_DELAY))
    encoderPulses = 0;
    
  encoderPulses++;
  if(motorStart == -1 && encoderPulses > START_PULSES){
    motorStart = time;
    Serial.println("Motor start");
  } else {
    currSpeed = 1.0/(time-lastMotor);
  }
  
  lastMotor = time; 
}
