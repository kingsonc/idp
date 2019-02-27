#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor_L = AFMS.getMotor(1);
Adafruit_DCMotor *Motor_R = AFMS.getMotor(2);

void decoder(String cmd) {
  if (cmd.charAt(0) == 'M') {
    Serial.print('M');
    // Motor instruction
    int spd = cmd.substring(3,6).toInt();
    Serial.print(spd);
    if (cmd.charAt(1) == 'L') {
      Serial.print('L');
      Motor_L->setSpeed(spd);
    } else if (cmd.charAt(1) == 'R'){
      Serial.print('R');
      Motor_R->setSpeed(spd);
    }      
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  
  pinMode(13, OUTPUT);
  AFMS.begin();

  Motor_L->setSpeed(0);
  Motor_R->setSpeed(0);
  
  Motor_L->run(FORWARD);
  Motor_R->run(FORWARD);
}

void loop() {
  if (Serial.available() > 0) {
    String rc = Serial.readStringUntil('.');
    Serial.print(rc);
    int delimiterIdx = rc.indexOf(',');
    while (delimiterIdx > 0) {
      String cmd = rc.substring(0,delimiterIdx);
      Serial.print(cmd);
      decoder(cmd);
      rc.remove(0, delimiterIdx+1);
      delimiterIdx = rc.indexOf(',');
    }
    Serial.println('a');
  }
}
