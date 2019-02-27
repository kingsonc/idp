/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  myservo.attach(10);  // attaches the servo on pin 9 to the servo object
  pos = myservo.read();
  Serial.println("Servo now at: ");
  Serial.print(pos);
  Serial.println("Zeroing");
  myservo.write(90);
}

void loop() {
  if (pos <= 180, ) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(180);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  if (hall_effect == 48) { // goes from 180 degrees to 0 degrees
    myservo.write(0);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}
