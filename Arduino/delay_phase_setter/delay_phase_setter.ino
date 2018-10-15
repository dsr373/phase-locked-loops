// program that generates two square waves based on the half-period received as a serial port input
// input is in microseconds
// the waves are out of phase by a factor also received as serial input
// this is given in degrees (0 to 360)

// variables
unsigned long t = 125; // wait time
unsigned long phase_diff = 0; // the phase difference in 10^-4 of 180 degrees (i.e. 1e4 -> 180 deg)
String string_read; // value read from serial

unsigned long t1_ahead, t2_behind; // the time that only 

// global constants
const int pin = 13; // the pin to generate the signal on
const int pin2 = 10; // the second pin, which is out of phase
const int pinmask = (1 << (pin-8));  // pin 1 bitmaks
const int pinmask2 = (1 << (pin2-8));  // pin 2 bitmask
const int bitmask = pinmask | pinmask2 ; // the port covers bits from 8 to 13, so that's why minus 8

// the function pointer to use to wait
void (*waitfunc)(unsigned long) = &delay;

void setup() {
  DDRB = bitmask;
  Serial.begin(9600);
  // noInterrupts(); // for some reason this messes up EVERYTHING
  // cli();
}

void loop() {
  if(Serial.available()) {
    string_read = Serial.readString();
    string_read.trim();
    Serial.println(String("read: ") + string_read);

    parseInput(string_read);
  }

  // on and off
  PORTB = pinmask;      // set pin 1
  waitfunc(t1_ahead);   // wait a fraction of t
  PORTB = bitmask;      // set both
  waitfunc(t2_behind);  // wait the rest of t
  PORTB = pinmask2;     // set just the second pin
  waitfunc(t1_ahead);   // wait a fraction of t
  PORTB = 0;            // reset both
  waitfunc(t2_behind);
}

void parseInput(String received) {
  unsigned long value_read = 0;
  
  if(received.startsWith("f")) {
    // here setting frequency
    value_read = received.substring(1).toInt();

    // here set in microseconds and use the us function
    if(value_read >= 1 && value_read < 16000) {
      t = value_read;
      setTimes();
      waitfunc = &myDelayMicroseconds;
      Serial.println(String("updated period: ") + String(t) + String("us"));
    }

    // here set in milliseconds and use the ms function
    else if(value_read >= 16000 && value_read < 1000000) {
      t = value_read / 1000;
      setTimes();
      waitfunc = &delay;
      Serial.println(String("updated period: ") + String(t) + String("ms"));
    }
  }
  
  else if(received.startsWith("p")) {
    // here setting phase
    value_read = received.substring(1).toInt();
    if(value_read >= 0 && value_read <=180) {
      phase_diff = value_read * 10000 / 180;
      Serial.println(String("updated phase diff: ") + String(value_read) + String(" deg"));
      setTimes();
    }
  }
}

inline void setTimes() {
  t1_ahead = t * phase_diff / 10000;
  t2_behind = t - t1_ahead;
}

inline void myDelayMicroseconds(unsigned long us) {
  // this is a terrible hack
  // basically the types of delay and delayMicroseconds don't match
  // so therefore I need to define this to be able to assign them to the function pointer
  delayMicroseconds((unsigned int)us);
}
