#include <Adafruit_MotorShield.h>

const byte MOV_LED = 6;
const byte SWITCH = 3;
volatile byte a = LOW;

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *Motor_R = AFMS.getMotor(1);
Adafruit_DCMotor *Motor_L = AFMS.getMotor(2);
Adafruit_DCMotor *Motor_Tip = AFMS.getMotor(3);


void b() {
  a = !a;
  Serial.println("output");
}

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
  Serial.println("tipping");
}

void setup() {
  AFMS.begin();
  Serial.begin(9600);                           //initialise serial
  Serial.setTimeout(500);
  Serial.write("READY");

  pinMode(SWITCH, INPUT);
  attachInterrupt(digitalPinToInterrupt(SWITCH), b, RISING); 
}

void loop() {
  Serial.println("Hello My Name is Becky... PLease Feed Me!");
  delay(1000);
}
