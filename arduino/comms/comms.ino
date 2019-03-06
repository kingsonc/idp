void decoder(String rc) {
  if (rc.charAt(0) == 'L') {
    digitalWrite(13, HIGH);
  } else {
    digitalWrite(13, LOW);
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("<Arduino is ready>");
  
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String rc = Serial.readStringUntil('.');
    decoder(rc);
    Serial.println(rc);
  }
}
