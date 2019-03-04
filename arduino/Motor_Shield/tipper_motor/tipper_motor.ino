#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *Motor_1 = AFMS.getMotor(1);


//Setup and Loop
void setup() {
  AFMS.begin();
  Motor_Tip->setSpeed(255);
  Motor_Tip->run(FORWARD);
  delay(2050); //Raise for set amount of time
  Motor_Tip->setSpeed(50); //Hold Motor Steady
  delay(500);
  Motor_Tip->run(RELEASE); //Release Motor
}

void loop() {
  //initialise adafruit 

}
