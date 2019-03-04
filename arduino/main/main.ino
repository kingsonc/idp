#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object and set addresses.
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor_L = AFMS.getMotor(1);
Adafruit_DCMotor *Motor_R = AFMS.getMotor(2);
Adafruit_DCMotor *Motor_Tip = AFMS.getMotor(3);

//Create Servo Object
Servo propeller;
int propeller_pin = 9

//define analog beam break input
int photodiode=A0;
bool block_in_working_area = false;

//define hall effect pin
int hall_effect_pin=A1;
bool is_magnetic=false;

//Serial Communications Protocol
char delimiter = ',';
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

//define slow movement forwards
void slow_movement() {
    Motor_L->setSpeed(100);
    Motor_R->setSpeed(100);
    Motor_L->run(FORWARD);
    Motor_R->run(FORWARD);
}

//define motor stop
void stop_motors() {
  Motor_L->setSpeed(0);
  Motor_R->setSpeed(0);
  Motor_L->run(FORWARD);
  Motor_R->run(FORWARD);
}

//Beam Break Testing Subroutine
void beam_break() {
  int val = analogRead(photodiode);
  if (val >= 700) {                                   //set threshold
       Serial.println("There is a block in the way!");
       block_in_working_area = true;
  }
  else {
        block_in_working_area=false;
  }
}

//Hall Effect Testing Subroutine
void hall_effect() {
  int magnetic = analogRead(hall_effect_pin);
  int threshold = 350-magnetic;
    if (abs(threshold) >=50) {                          //set threshold
      is_magnetic = true;
    }
    else {
      is_magnetic = false;
    }
}

//Accept and reject mechanism
void servo_accept(){
  slow_movement();
  delay(3);                         
  propeller.write(180);              // tell servo to go to 180 ****NEEDS CHANGING***
  Serial.print("Block Accepted");
}

void servo_reject() {
  slow_movement();
  delay(3);                         
  propeller.write(0);               // tell servo to go to 0  ****NEEDS CHANGING***
  Serial.print("Block Rejected");
}

void tipper() {
  Motor_Tip->setSpeed(255);
  Motor_Tip->run(FORWARD);
  delay(2050); //Raise for set amount of time
  Motor_Tip->setSpeed(50); //Hold Motor Steady
  delay(500);
  Motor_Tip->run(RELEASE); //Release Motor
}

//Setup and Loop
void setup() {
  //initialise photodiode pin input
  pinMode(photodiode,INPUT); 
  
  //initialise servo object
  propeller.attach(propeller_pin);       

  //Initialise Motors
  AFMS.begin();
  stop_motors();
  Serial.begin(9600);        //initialise serial
  Serial.write("Arduino is Ready.");
}

void loop() {
    //initialise adafruit 
    AFMS.begin();

    //set new motor speed
    cmd = Serial.readStringUntil(delimiter);
    decoder(cmd);
    
    //test beam break and hall effect
    beam_break();
    hall_effect();
    if (block_in_working_area == true && is_magnetic==false) {
      servo_accept();               //accept block
      is_magnetic = false;          //reset
      block_in_working_area = false;
    }
    else if (block_in_working_area == true && is_magnetic==true) {
      servo_reject();               //reject block
      is_magnetic = false;          //reset
      block_in_working_area = false;
    }
  }  
