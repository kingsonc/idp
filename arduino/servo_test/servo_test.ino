#include <Servo.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *Motor_Tip = AFMS.getMotor(3);


Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void servo_accept(){
  for (pos = 50; pos<=180; pos+=1){
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(8);
  } 
}

void servo_reject(){
  for (pos = 100; pos>=0; pos-=1){
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(10);
  } 
}

void tip() {
  Motor_Tip->setSpeed(255);
  Motor_Tip->run(FORWARD);
  delay(1800); //Raise for set amount of time
  Motor_Tip->run(BACKWARD); //Release Motor
  Motor_Tip->setSpeed(50); //Hold Motor Steady
  delay(500);
  Motor_Tip->setSpeed(200);
  delay(500);
  Motor_Tip->run(RELEASE);
}

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  AFMS.begin();
  //myservo.write(85);
  myservo.write(60);
}

void loop() {
}
