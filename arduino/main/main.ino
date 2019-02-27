#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *Motor_1 = AFMS.getMotor(1);
// You can also make another motor on port M2
Adafruit_DCMotor *Motor_2 = AFMS.getMotor(2);

//Create Servo Object
Servo propeller;

//define analog photodiode input
int photodiode=A0;

//declare variables needed later on
String rc;
boolean newData = false;
int rcv_spd;
char rcvd_dirn;
int pos = 0;    // variable to store the servo position

//Serial Communications Protocol
//Print new serial data
void showNewData() {
     rcvd_dirn = rc.charAt(0);
     rc.remove(0,1);
     rcv_spd = rc.toInt();
     Serial.println(rcvd_dirn);
     Serial.println(rcv_spd);
     newData = false;
}

// Receive Serial Data
void recvWithStartEndMarkers() {
    char startMarker = '<';
    char endMarker = '>';
    
  if (Serial.available() > 0) {
      rc = Serial.readStringUntil(endMarker);
      if (rc.charAt(0)== 60){
        rc.remove(0,1);
        newData = true;
      }
  }
}

//declare functions to move forwards, backwards, left and right turns.
//Move Forwards
void forwards(int spd) {
  //set default speeds
  Motor_1->setSpeed(spd);
  Motor_2->setSpeed(spd);

  //move forward
  Motor_1->run(FORWARD);
  Motor_2->run(FORWARD);
  delay(500);
  
  Motor_1->run(RELEASE);
  Motor_2->run(RELEASE);
}

//Left Turn
void left_turn(int spd) {
  //set default speeds
  Motor_1->setSpeed(spd);
  Motor_2->setSpeed(spd);

  //turn left
  Motor_1->run(FORWARD);
  //Motor_2->run(BACKWARD);
  delay(500);
  
  Motor_1->run(RELEASE);
  Motor_2->run(RELEASE);
}

//Right Turn
void right_turn(int spd) {
  //set default speeds
  Motor_1->setSpeed(spd);
  Motor_2->setSpeed(spd);
  
  //turn right
  //Motor_1->run(BACKWARD);
  Motor_2->run(FORWARD);
  delay(500);
  
  Motor_1->run(RELEASE);
  Motor_2->run(RELEASE);
}

//Reverse
void reverse(int spd) {
  //set default speeds
  Motor_1->setSpeed(spd);
  Motor_2->setSpeed(spd);
  
  //reverse
  Motor_1->run(BACKWARD);
  Motor_2->run(BACKWARD);
  delay(500); //500ms continuous running
  
  Motor_1->run(RELEASE);
  Motor_2->run(RELEASE);
}

void servo_accept(){
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    propeller.write(pos);              // tell servo to go to position in variable 'pos'
    delay(3);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    propeller.write(pos);              // tell servo to go to position in variable 'pos'
    delay(3);                       // waits 15ms for the servo to reach the position
  }                                 // waits for the servo to get there
}

//Setup and Loop
void setup() {
  pinMode(photodiode,INPUT); //initialise photodiode pin input
  propeller.attach(9);       //initialise servo object
  Serial.begin(9600);        //initialise serial
  while (!Serial) {
   ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.write("Connected!");
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

    //hall effect condition !!!!!!!!!!!!!!!!!!
    //accept 
    if (hall_effect==1) {
      servo_accept();  
    }

    //reject
    else if (hall_effect==0) {
      //servo_reject();  
    }
  }
  
  //receive new commands
  recvWithStartEndMarkers();
  if (newData == true) {
      showNewData();
      //everything else that depends on rc goes here
      if (rcvd_dirn == 119) { //decimal ascii code for w
         Serial.println("moving forwards");
         forwards(rcv_spd);
      }
    
      else if (rcvd_dirn == 115) { //decimal ascii code for s
         Serial.println("moving backwards");
         reverse(rcv_spd);
      }
    
      else if (rcvd_dirn == 97) { //decimal ascii for a
         Serial.println("turning left");
         left_turn(rcv_spd);
      }
    
      else if (rcvd_dirn == 100) { //decimal ascii for d
         Serial.println("turning right");
         right_turn(rcv_spd);
      }
  }
}
