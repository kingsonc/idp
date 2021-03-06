#include <Ticker.h>
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object and set addresses.
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor_R = AFMS.getMotor(1);
Adafruit_DCMotor *Motor_L = AFMS.getMotor(2);
Adafruit_DCMotor *Motor_Tip = AFMS.getMotor(3);
int spd = 0;

//define switch and LED pins
int SWITCH = 3;
bool tipped_already = false;
int MOV_LED = 6;
int STATE = LOW;

void led_blinky(){
  STATE = digitalRead(MOV_LED);
  STATE = !STATE;
  digitalWrite(MOV_LED, STATE);
}

Ticker movement_LED(led_blinky, 1000);

//Create Servo Object
Servo myservo;
int servo_pin = 9;

//define analog beam break input
int photodiode=A0;
bool block_in_working_area = false;
int beam_threshold = 390;
int block_counter = 23;

//define hall effect pin
int hall_effect_pin=A1;
bool is_magnetic=false;
int mag_threshold = 660;

//Serial Communications Protocol
char delimiter = ',';
char end_delimiter = '.';

//Print new serial data
void decoder(String cmd) {
  //turn anroud on spot and reverse
  if (cmd.charAt(0) == 'R') {
    block_counter = 0;
    Motor_L->setSpeed(80);
    Motor_R->setSpeed(80);
    Motor_L->run(BACKWARD);
    Motor_R->run(FORWARD);
    delay(4000);
    pre_saturation();
    delay(30000);    
    Serial.println("TC");
  }

  //usual protocol
  else if (cmd.charAt(0) == 'M') {
    if (cmd.charAt(1) == 'T') {
      int duration = cmd.substring(3,7).toInt();
      if (cmd.charAt(2) == 'L') {
        Motor_L->setSpeed(80);
        Motor_R->setSpeed(80);
        Motor_L->run(BACKWARD);
        Motor_R->run(FORWARD);
      } else if (cmd.charAt(2) == 'R') {
        Motor_L->setSpeed(80);
        Motor_R->setSpeed(80);
        Motor_L->run(FORWARD);
        Motor_R->run(BACKWARD);     
      }
      delay(duration);
      Serial.println("TC");
      slow_movement();
    }    
    
    else {
        spd = cmd.substring(3,6).toInt(); //slice bits 3-6 from serial (speed)
      
      //set motor speeds using commands received from serial
      if (cmd.charAt(1) == 'L') {
        Motor_L->setSpeed(spd);
      
        //check direction
        if (cmd.charAt(2) == 'F') {
          Motor_L->run(FORWARD);
        } else if (cmd.charAt(2) == 'R') {
          Motor_L->run(BACKWARD);
        }       
      } else if (cmd.charAt(1) == 'R' ){
        Motor_R->setSpeed(spd);
      
        //check direction
        if (cmd.charAt(2) == 'F') {
          Motor_R->run(FORWARD);
        } else if (cmd.charAt(2) == 'R') {
          Motor_R->run(BACKWARD);
        }  
      }
    }
  }
}


//define slow movement forwards
void slow_movement() {
  spd = 40;
  Motor_L->setSpeed(40);
  Motor_R->setSpeed(40);
  Motor_L->run(FORWARD);
  Motor_R->run(FORWARD);
}

//define reverse
void pre_saturation() {
    Motor_L->setSpeed(90);
    Motor_R->setSpeed(90);
    Motor_L->run(BACKWARD);
    Motor_R->run(BACKWARD);
}

//define motor stop
void stop_motors() {
  spd = 0;
  Motor_L->setSpeed(0);
  Motor_R->setSpeed(0);
  Motor_L->run(FORWARD);
  Motor_R->run(FORWARD);
}

//Beam Break Testing Subroutine
void beam_break() {
//  int val = analogRead(photodiode);
  int count = 0;
  while (analogRead(photodiode) >= beam_threshold) {                                   //set threshold
    count++;
    if (count>5) {
      block_in_working_area = true;
      break;
    }
  }
  
//       Serial.println("There is a block in the way!");
//       block_in_working_area = true;
//  }
//  else {
//        block_in_working_area=false;
//  }
}

//Hall Effect Testing Subroutine
bool hall_effect() {
  int magnetic = analogRead(hall_effect_pin);
    if (magnetic <= mag_threshold) {                          //set threshold
      return true;
    } else {
      return false;
    }
}

//Accept and reject mechanism
void servo_accept(){
  slow_movement();
  myservo.write(40);
  //Serial.print("ACCEPT");
  delay(1700); 
                          
  // sweep out
  for (int pos = 40; pos<=180; pos+=1){
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(5);
  } 
    
  //reset servo
  myservo.write(85);
}

void servo_reject() {
  //reset servo
  myservo.write(85);
  slow_movement();
  //Serial.print("REJECT");
  delay(3000);
}

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
  delay(850);
  Motor_Tip->run(BACKWARD);
  delay(30);
  Motor_Tip->run(FORWARD);
  delay(30);
  Motor_Tip->run(BACKWARD);
  delay(30);
  Motor_Tip->run(FORWARD);
  delay(200);
  Motor_Tip->setSpeed(50);
}

void tipper_landing() {
  Motor_Tip->run(BACKWARD);
  delay(800);
  Motor_Tip->run(RELEASE);
  delay(500);
}

//Setup and Loop
void setup() {
  //initialise pin inputs
  pinMode(photodiode,INPUT); 
  pinMode(MOV_LED,OUTPUT);
  pinMode(SWITCH, INPUT);

  //auto-calibration
  beam_threshold = analogRead(photodiode)+10;
  mag_threshold = analogRead(hall_effect_pin)-20;

  //initialise servo object and set to neutral
  myservo.attach(servo_pin);
  myservo.write(85);       

  //Initialise Motors
  AFMS.begin();
  stop_motors();
  tipper_landing();
  tipper_liftoff();
  Serial.begin(9600);                           //initialise serial
  Serial.println(beam_threshold);
  Serial.setTimeout(500);
  Serial.write("READY");

  movement_LED.start(); //it will start the ticker
}

void loop() {
  if (Serial.available() > 0) {
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
  }

  //test beam break and hall effect
  beam_break();
  //Serial.println(analogRead(photodiode));

  //if moving, set LED high
  if(spd != 0){
      movement_LED.update(); //resume the ticker.
  }
  if(spd == 0){
      digitalWrite(MOV_LED, LOW);
  }

  //test block in working area
  if (block_in_working_area == true) {
    slow_movement();
    for (int i=0; i<=720; i++){
      bool check = hall_effect();
      if(check==true){
        is_magnetic = true;
        break;
      }
      delay(1);
    }

    if(is_magnetic==false && block_counter > 0) {
      myservo.write(40);  
      tipper_landing();
      servo_accept();
      delay(150);
      tipper_liftoff();   //accept block, send serial
      block_counter -= 1;
    } 
    
    else if (is_magnetic == true) {
      servo_reject();     //reject block, send serial
      block_counter -= 1;
    }

    //reset
    is_magnetic = false;         
    block_in_working_area = false;  
    slow_movement();
  }

  if (digitalRead(SWITCH) == HIGH && tipped_already == false) {
    tip();
    tipped_already = true;
    tipper_liftoff();
    slow_movement();
    delay(5000);
    Serial.println("TIP");
  }
}
