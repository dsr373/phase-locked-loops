// this code generates a pulsed signal for controlling the circuit

void setup() {
  // put your setup code here, to run once:
  DDRB = B100000;
  cli();    // very important -- disables interrupts, to the frequency is actually kind of correct
}

void loop() {
  // put your main code here, to run repeatedly:
  PORTB = B100000;
  delayMicroseconds(500);
  PORTB = 0;
  delayMicroseconds(500);
}
