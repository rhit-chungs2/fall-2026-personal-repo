String inputString = "";      // a String to hold incoming data
bool isStringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(19200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);

  pinMode(13,OUTPUT);

}

void loop() {
  // print the string when a newline arrives:
  if (isStringComplete) {

    if(inputString.equals("LED ON")){
      digitalWrite(13,HIGH);
      Serial.println("The LED is now on!");

    }else if(inputString.equals("LED OFF")){
    digitalWrite(13,LOW);
    Serial.println("The LED is now off!");
    }else if (inputString.startsWith("FLASH")) {
    handleFlash(inputString.substring(5));
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

void handleFlash(String inputline){
  inputline.trim();
  int firstSpace = inputline.indexOf(' ');
  String num1 = inputline.substring(0,firstSpace);
  String num2 = inputline.substring(firstSpace+1);

  int num  = num1.toInt();
  int period = num2.toInt();
  Serial.println("Flashes = " + String(num) + " PeriodMS = " + String(period));
  //Serial.print("Number of times:");
  //Serial.println(num);
  //Serial.print("Period of:");
  //Serial.println(period);
  for (int i=0; i<num; i++){
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(period/2);                      
  digitalWrite(LED_BUILTIN, LOW);   
  delay(period/2);
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
