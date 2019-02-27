#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object and set addresses.
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor_L = AFMS.getMotor(1);
Adafruit_DCMotor *Motor_R = AFMS.getMotor(2);

//Create Servo Object
Servo propeller;

//define analog beam break input
int photodiode=A0;

//define hall effect pin
int hall_effect_pin=A1;
bool is_magnetic=false;

//Serial Communications Protocol
//Print new serial data
void decoder(String cmd) {
  if (cmd.charAt(0) == 'M') {
    int spd = cmd.substring(3,6).toInt(); //slice bits 3-6 from serial (speed)
     
     //set motor speeds using commands received from serial
     if (cmd.charAt(1) == 'L') {
      Motor_L->setSpeed(spd);
    } else if (cmd.charAt(1) == 'R'){
      Motor_R->setSpeed(spd);
    }      
  }
}

void slow_movement() {
    Motor_L->setSpeed(100);
    Motor_R->setSpeed(100);
    Motor_L->run(FORWARD);
    Motor_R->run(FORWARD);

}

void hall_effect() {
  int threshold = 700
    int magnetic = analogRead(hall_effect_pin);
      if (magnetic >= threshold) {
        is_magnetic = true;
      }
      else{
        is_magnetic = false;
      }
}

//Accept and reject mechanism
void servo_accept(){
  slow_movement();
  delay(3);                         
  propeller.write(180);              // tell servo to go to 180 ****NEEDS CHANGING***
}

void servo_reject() {
  slow_movement();
  delay(3);                         
  propeller.write(0);               // tell servo to go to 0  ****NEEDS CHANGING***
}

//Setup and Loop
void setup() {
  //initialise photodiode pin input
  pinMode(photodiode,INPUT); 
  
  //initialise servo object
  propeller.attach(9);       

  //Initialise Motors
  AFMS.begin();
  Motor_L->setSpeed(0);
  Motor_R->setSpeed(0);
  Motor_L->run(FORWARD);
  Motor_R->run(FORWARD);
  
  Serial.begin(9600);        //initialise serial
  Serial.write("Arduino is Ready.");
}

void loop() {
  //initialise adafruit 
  AFMS.begin();

  //beam break
  int val = analogRead(photodiode);
  if (val >= 700) {
    //run subroutine here
    Serial.println("There is a block in the way!");
    //move motors a little
    hall_effect();
    if (is_magnetic==true) {
      servo_accept();               //accept block
      is_magnetic = false;          //reset
    }
    else if (is_magnetic==false) {
      servo_reject();               //reject block
      is_magnetic = false;          //reset
    }
  }  
}
