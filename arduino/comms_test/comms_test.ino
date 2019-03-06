String rc;
boolean newData = false;
int rcv_spd;
char rcvd_dirn;

void recvWithStartEndMarkers() {
    char startMarker = '<';
    char endMarker = '>';

  if (Serial.available() > 0) {
      rc = Serial.readStringUntil(endMarker);
      if (rc.charAt(0)== 60){
        rc.remove(0,1);
        newData = true;
      }
  }
}

void showNewData() {
     rcvd_dirn = rc.charAt(0);
     rc.remove(0,1);
     rcv_spd = rc.toInt();
     Serial.println(rcvd_dirn);
     Serial.println(rcv_spd);
     newData = false;
}

void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");
}

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
      showNewData();
      //everything else that depends on rc goes here
  }
}
