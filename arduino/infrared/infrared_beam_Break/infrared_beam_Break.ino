 int photodiode=A0; //define analog photodiode input
 
 void setup(){  
  pinMode(photodiode,INPUT);  
  Serial.begin(9600);          //set serial monitor at a default baund rate of 9600  
 }  
 void loop() {   
  int val = analogRead(A0);
  Serial.println(val);          // prints the values from the sensor in serial monitor  
  if (val >= 700) {
    //run subroutine here
    Serial.println("There is a block in the way!");
  }
  
  delay(100);
  }  
