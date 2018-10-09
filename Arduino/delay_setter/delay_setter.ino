// program that generates a square wave based on the half-period
// which is received as a serial port input
// input is in microseconds

// variables
unsigned long t = 125; // wait time
unsigned long value_read = 0; // value read from serial

int pin = 13;
int bitmask = 1 << (pin-8);

// the function pointer to use to wait
void (*waitfunc)(unsigned long) = &delay;

void setup() {
  DDRB = bitmask;
  Serial.begin(9600);
  // noInterrupts(); // for some reason this messes up EVERYTHING
}

void loop() {
  if(Serial.available()) {
    value_read = Serial.parseInt();
    Serial.println(String("read: ") + String(value_read));

    // here set in microseconds and use the us function
    if(value_read >= 1 && value_read < 16000) {
      t = value_read;
      waitfunc = &delayMicroseconds;
      Serial.println(String("updated period: ") + String(t) + String("us"));
    }

    // here set in milliseconds and use the ms function
    else if(value_read >= 16000 && value_read < 1000000) {
      t = value_read / 1000;
      waitfunc = &delay;
      Serial.println(String("updated period: ") + String(t) + String("ms"));
    }
  }

  // on and off
  PORTB = bitmask;
  waitfunc(t);
  PORTB = 0;
  waitfunc(t);
}
