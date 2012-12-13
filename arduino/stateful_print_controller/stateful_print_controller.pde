#include "stateful_print_controller.h"
#include <Servo.h> 

unsigned long feed_time = -1;
//int feed_count = 0;

unsigned long firstMotor = -1;
unsigned long lastMotor = -1; 

unsigned long encoderPulses = 0;

STATES currState;
InputState inputStates[5] = { { 0, 0 }, { 0, 0 }, { 0, 0 }, { 0, 0 }, { 0, 0 } };

Servo frontServo;
Servo backServo;

void setup(){
  pinMode(FEED_PIN, INPUT);
  pinMode(PAPER_PIN, INPUT);
  pinMode(PWR_BUTTON_PIN, INPUT); // Set to output when we want to use is
  pinMode(PWR_LIGHT_PIN, INPUT);
  pinMode(ERR_LIGHT_PIN, INPUT);

  attachInterrupt(MOTOR_INT, trackMotor, CHANGE);
  
  stopPrintFeed();
  
  currState = OFF;
  
  Serial.begin(9600);
  Serial.print(currState);
}

void loop(){
  updateInputStates();
  STATES oldState = currState;

  // Power management
  if(currState == OFF && getState(SERIAL_READ) == PRINT_ENABLE){
    togglePower();
    delay(1000);
    setInput(PWR_LIGHT, 1); // Fake it
  } else if(currState == STANDBY &&
            getState(SERIAL_READ) == PRINT_DISABLE &&
            getTime(SERIAL_READ) > SLEEP_DELAY){
    togglePower();
    setInput(PWR_LIGHT, LOW); // Fake it
  }
  
  // State transition management
  if(getState(ERR_LIGHT)){
    currState = ERROR;
  } else if(!getState(PWR_LIGHT) && getTime(PWR_LIGHT) > PWR_TIME) {
    currState = OFF;
  } else if((currState == OFF && getState(PWR_LIGHT)) || (currState == STANDBY && !getState(PWR_LIGHT))){ // !(currState == OFF || currState == ERROR || getState(PWR_LIGHT))
    currState = STARTSTOP;
  } else {
    switch(currState){
      case OFF:
        if(getState(PWR_LIGHT))
          currState = STARTSTOP;
        break;
      case STARTSTOP:
        if(getTime(PWR_LIGHT) > PWR_TIME){
          if(getState(PWR_LIGHT)){
            currState = STANDBY;
          } else {
            currState = OFF; // Duplicates code above
          }
        }
        break;
      case STANDBY:
        if(getState(SERIAL_READ) == PRINT_ENABLE ||
           getState(SERIAL_READ) == PRINT_START)
           currState = READY;
        break;
      case READY:
        if(getState(SERIAL_READ) == (int)PRINT_DISABLE){
          currState = STANDBY;
        } else if(getState(FEED) && getTime(FEED) > FEED_DELAY){
          currState = FED;
        }
        break;
      case FED:
        if(getState(SERIAL_READ) == (int)PRINT_DISABLE){
          currState = STANDBY;
        } else if(!getState(MOTOR) && getTime(MOTOR) > START_WAIT_TIME){
          currState = PRINT;
        }
        break;
      case PRINT:
        if((!getState(MOTOR) && getTime(MOTOR) > CLEAR_WAIT_TIME) ||
            (getState(MOTOR) && getTime(MOTOR) > MAX_FEED_TIME)){
          currState = CLEAR;
        } 
        break;
      case CLEAR:
        if(getState(MOTOR) && getTime(MOTOR) > CLEAR_FEED_TIME){
          currState = STANDBY;
          setInput(SERIAL_READ, 0);
        }
        break;
      case ERROR:
        // Only place to go is OFF, defined elsewhere
        break;
    } 
  }
  
  // State transistion handling
  if(currState != oldState){
    Serial.print(currState);
    switch(currState){
      case OFF:
        // TODO: Turn off servos?
        frontServo.detach();
        backServo.detach();
        break;
      case STARTSTOP:
        frontServo.attach(FRONT_SERVO_PIN);
        backServo.attach(BACK_SERVO_PIN);
        stopPrintFeed();
        break;
      case ERROR:
        setInput(SERIAL_READ, 0);
        stopPrintFeed();
        togglePower();
        break;
      case STANDBY:
        stopPrintFeed();
        break;
      case READY:
        attachInterrupt(FEED_INT, recordFeed, FALLING);
        setInput(FEED, 0);
        break;
      case FED:
        pinMode(PAPER_PIN, OUTPUT);
        digitalWrite(PAPER_PIN, LOW);
        detachInterrupt(FEED_INT);
        break;
      case PRINT:
        frontServo.write(ON_FRONT_SERVO);
        backServo.write(ON_BACK_SERVO);
        break;
      case CLEAR:
        frontServo.write(OFF_FRONT_SERVO);
        backServo.write(OFF_BACK_SERVO);
        break;
    }
  }
}

void recordFeed(){
  inputStates[FEED].state = 1;
  inputStates[FEED].start = millis();
}

void togglePower(){
  digitalWrite(PWR_BUTTON_PIN, LOW);
  pinMode(PWR_BUTTON_PIN, OUTPUT);
  delay(PWR_BUTTON_DELAY);
  pinMode(PWR_BUTTON_PIN, INPUT);
}

void stopPrintFeed(){
  frontServo.write(OFF_FRONT_SERVO);
  backServo.write(OFF_BACK_SERVO);
  pinMode(PAPER_PIN, INPUT);
  detachInterrupt(FEED_INT);
}

char getState(INPUTS input){
  return inputStates[input].state;
}

unsigned long getTime(INPUTS input){
  return millis() - inputStates[input].start;
}

void setInput(INPUTS input, char state){
  setInput(input, state, millis());
}

void setInput(INPUTS input, char state, unsigned long time){
  
  if(inputStates[input].state != state){
    inputStates[input].state = state;
    inputStates[input].start = millis();
  }
}

char charDigitalRead(int pin){
  if(digitalRead(pin) == HIGH)
    return 1;
  else
    return 0;
}

void updateInputStates(){
  if((lastMotor + OFF_DELAY) < millis()){
    setInput(MOTOR, 0);
    encoderPulses = 0;
  } else if((encoderPulses > START_PULSES) && 
            (lastMotor - firstMotor) > MIN_MOTOR_TIME) {
    setInput(MOTOR, 1);
  }
  
  setInput(PWR_LIGHT, charDigitalRead(PWR_LIGHT_PIN));
  setInput(ERR_LIGHT, charDigitalRead(ERR_LIGHT_PIN));
  
  if(Serial.available() > 0){
    char incoming = Serial.read();
    if(incoming > 10){
      incoming -= 48;
    }
    setInput(SERIAL_READ, incoming);
  }
  
  if(currState != READY)
    setInput(FEED, 0);
  
}

void trackMotor(){
  long time = millis();
  
  if(encoderPulses == 0)
    firstMotor = time;
    
  encoderPulses++;
  lastMotor = time; 
}
