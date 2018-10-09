// this code generates a pulsed signal for controlling the circuit

// variable declaration
int pin = 13;

void setup() {
  // put your setup code here, to run once:
  pinMode(pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(pin, HIGH);
  delayMicroseconds(500);
  digitalWrite(pin, LOW);
  delayMicroseconds(500);
}
