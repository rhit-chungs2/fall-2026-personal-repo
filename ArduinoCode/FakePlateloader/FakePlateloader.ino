String inputString = "";      // a String to hold incoming data
bool isStringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(19200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);


}

void loop() {
  // print the string when a newline arrives:
  if (isStringComplete) {

    if(inputString.equals("RESET")){
      delay(500);
      Serial.println("READY, SAGIAN PE Loader, ROM Ver. 1.16, 12APR2001");

    }else if(inputString.startsWith("MOVE")){
      delay(3000);
      Serial.println("READY");
    }else if(inputString.equals("GRIPPER OPEN")){
      Serial.println("READY, OPEN");
    }else if(inputString.equals("GRIPPER CLOSE")){
      Serial.println("READY, CLOSED NO PLATE");
    }else if(inputString.equals("Z-AXIS EXTEND")){
      Serial.println("READY,EXTENDED");
    }else if(inputString.equals("Z-AXIS RETRACT")){
      Serial.println("READY,RETRACTED");
    }else if(inputString.startsWith("X-AXIS")){
      Serial.println("READY");
    }else{
      Serial.print("Unknown command -->");
      Serial.println("inputString");
    }
    //TODO: Do the command
    // clear the string:
    inputString = "";
    isStringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      isStringComplete = true;
    }else{
      inputString += inChar;
    }
  }
}
