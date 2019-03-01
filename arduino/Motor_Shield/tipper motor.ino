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


//Setup and Loop
void setup() {
  AFMS.begin();
  Motor_1->setSpeed(255);
  Motor_1->run(FORWARD);
  delay(2050); //500ms continuous running
  Motor_1->setSpeed(50);
  delay(500);
  Motor_1->run(RELEASE);
}

void loop() {
  //initialise adafruit 

}
