int PIN = 9;


void setup(){
  Serial.begin(9600);
  pinMode(PIN, INPUT);
}

void loop(){
  Serial.println(digitalRead(PIN));
  delay(1000);
}
