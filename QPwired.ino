#include <SoftwareSerial.h>
#include <Servo.h>
int distraction = 0; // checks if you are looking away  1 = looking and 2 = looking away
String newTime; // Stores from serial port
int ledPin[] = {6, 7, 8, 9, 10, 11, 12}; 
int buzzerPin = 5;
unsigned long timePassed; // amount of time you are looking away
unsigned long startMillis; // start time when you looked away
unsigned long currentMillis; // current time for when you looked away
const unsigned long fivesec = 5000;
const unsigned long tensec = 10000;
const unsigned long fifteensec = 15000;
Servo servo;
void setup() {
  //initialize arduino parts for arduino and set start timer
  Serial.begin(9600);
  startMillis = millis();
  pinMode(buzzerPin, OUTPUT);
  for (int i = 0; i<7; i++) 
{ 
  pinMode(ledPin[i], OUTPUT); // define LED pinmode for each LED
}
  servo.attach(4);
  servo.write(90);
}
void event() {
//reads data from serial moniter, updates distraction value if it changes, and keeps track of time looking/looking away
  if(Serial.available()!=0) {
    newTime = Serial.readStringUntil('x'); //read looking value from serial port
    currentMillis = millis(); //see how long it has been
    if (distraction != newTime.toInt()) {
      distraction = newTime.toInt(); //update if you are looking away or not
      startMillis = millis(); //update start timer
    }
  }
}

void ledTest() {
  // checks if you are looking away for a certain amount of time, and alerts you to pay attention by arduino parts
  if (distraction == 1){ //if looking at screen, turn off buzzer
    digitalWrite(buzzerPin, LOW);
  }
  if (distraction == 2){ //if looking away, see how much time you have been looking
    timePassed = currentMillis - startMillis; 
    if (timePassed >= fivesec) //if looking away for more than 5 sec, flash LEDs
    {
      for (int i = 0; i<7; i++) {
        digitalWrite(ledPin[i], HIGH);
        delay(10);
      }
      for (int i = 0; i<7; i++) {
        digitalWrite(ledPin[i], LOW);
        delay(10);
      }    
    }
    if (timePassed >= tensec) //if looking away for more than 10 sec, rotate servo to tap your wrist
    {
      servo.write(0);
      delay(100);
      servo.write(90); 
      delay(100);
    }    
    if (timePassed >= fifteensec) { //if looking away for more than 15 sec, turn buzzer on
      digitalWrite(buzzerPin, HIGH);
      delay(10);
    }
    else {
      digitalWrite(buzzerPin, LOW);
    }
  }
}
void loop() {
  ledTest();
  event();
}
