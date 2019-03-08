const byte ledPin = 6;
const byte interruptPin = 3;
volatile byte a = LOW;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), b, RISING);
}

void loop() {
  digitalWrite(ledPin, a);
}

void b() {
  a = !a;
}
