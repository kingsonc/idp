int analogPin = A0;     // Hall effect output voltage connected to A0
int val = 0;           // variable to store the value read

void setup()
{
  Serial.begin(9600);              //  setup serial
}

void loop()
{
  val = analogRead(analogPin);     // read the input pin
  //val = digitalRead(digitalPin);    //read digital pin (after schmidt trigger)
  Serial.println(val);             // debug value
} 
