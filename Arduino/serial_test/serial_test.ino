// var declarations
//int pin = 9;
int ledpin = 13;
String message = "";
String reply = "";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  pinMode(pin, OUTPUT);
  pinMode(ledpin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    message = Serial.readString();
    if(message == "on") {
      digitalWrite(ledpin, HIGH);
      reply = "pin 13 turned on";
    }
    else if(message = "off") {
      digitalWrite(ledpin, LOW);
      reply = "pin 13 turned off";
    }

    Serial.println(reply);
  }
}
