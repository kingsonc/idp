#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object and set addresses.
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor_R = AFMS.getMotor(1);
Adafruit_DCMotor *Motor_L = AFMS.getMotor(2);
Adafruit_DCMotor *Motor_Tip = AFMS.getMotor(3);

//Create Servo Object
Servo myservo;
int servo_pin = 9;

//define analog beam break input
int photodiode=A0;
bool block_in_working_area = false;

//define hall effect pin
int hall_effect_pin=A1;
bool is_magnetic=false;

//Serial Communications Protocol
char delimiter = ',';
char end_delimiter = '.';

//Print new serial data
void decoder(String cmd) {
  if (cmd.charAt(0) == 'M') {
    int spd = cmd.substring(3,6).toInt(); //slice bits 3-6 from serial (speed)
     
     //set motor speeds using commands received from serial
     if (cmd.charAt(1) == 'L') {
      Motor_L->setSpeed(spd);
      
      //check direction
      if (cmd.charAt(2) == 'F') {
        Motor_L->run(FORWARD);}  
      else if (cmd.charAt(2) == 'R'){
        Motor_L->run(BACKWARD);}       
      }
      
     else if (cmd.charAt(1) == 'R'){
      Motor_R->setSpeed(spd);
      
      //check direction
      if (cmd.charAt(2) == 'F') {
        Motor_R->run(FORWARD);}  
      else if (cmd.charAt(2) == 'R'){
        Motor_R->run(BACKWARD);}  
      }      
  }
}

//define slow movement forwards
void slow_movement() {
    Motor_L->setSpeed(75);
    Motor_R->setSpeed(75);
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
  myservo.write(60);
  Serial.print("ACCEPT");
  delay(1000); 
  stop_motors();                        
 
  // sweep out
  for (int pos = 50; pos<=180; pos+=1){
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(10);
  } 

  //reset servo
  myservo.write(85);
}

void servo_reject() {
  //reset servo
  myservo.write(85);
  slow_movement();
  Serial.print("REJECT");
}               
  /*// sweep out
  for (int pos = 100; pos>=0; pos-=1){
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(10);
  } 
}
*/

//tipper mechanism
void tip() {
  Motor_Tip->setSpeed(255);
  Motor_Tip->run(FORWARD);
  delay(2000); //Raise for set amount of time
  Motor_Tip->setSpeed(50); //Hold Motor Steady
  delay(2000);
  Motor_Tip->run(BACKWARD);
  Motor_Tip->setSpeed(200);
  delay(500);
  Motor_Tip->run(RELEASE);
}

void tipper_liftoff() {
  Motor_Tip->setSpeed(255);
  Motor_Tip->run(FORWARD);
  delay(200);
  Motor_Tip->setSpeed(50);
}

void tipper_landing() {
  Motor_Tip->run(BACKWARD);
  delay(250);
  Motor_Tip->run(RELEASE);
}

//Setup and Loop
void setup() {
  //initialise photodiode pin input
  pinMode(photodiode,INPUT); 
  
  //initialise servo object and set to neutral
  myservo.attach(servo_pin);
  myservo.write(85);       

  //Initialise Motors
  AFMS.begin();
  stop_motors();
  tipper_liftoff();
  Serial.begin(9600);                           //initialise serial
  Serial.setTimeout(500);
  Serial.write("READY");
}

void loop() {
    //set new motor speed
    String rc = Serial.readStringUntil(end_delimiter);
    int delimiterIdx = rc.indexOf(delimiter);
    while (delimiterIdx > 0) {
      String cmd = rc.substring(0,delimiterIdx);
      decoder(cmd);
      rc.remove(0, delimiterIdx+1);
      delimiterIdx = rc.indexOf(delimiter);
    }
    Serial.println('A');
    
    //test beam break and hall effect
//    beam_break();
    
    if (block_in_working_area == true) {
      hall_effect();                            //test hall effect
      
      if(is_magnetic==false) {
        tipper_landing();
        servo_accept();
        tipper_liftoff();}                       //accept block, send serial

      else if (is_magnetic == true) {
        servo_reject();}                         //reject block, send serial

      //reset
      is_magnetic = false;         
      block_in_working_area = false;  
    }

    //listen for tipping command
  }  
