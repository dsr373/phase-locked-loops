unsigned int pin = 10;
unsigned int duty_cycle = 128;

String read_string;

void setup() {
  // put your setup code here, to run once:
  pinMode(pin, OUTPUT);
  analogWrite(pin, duty_cycle);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {
    read_string = Serial.readString();
    read_string.trim();
    Serial.println(String("read: ") + read_string);

    parse_input(read_string);
  }
}

inline void parse_input(String read_string) {
  unsigned long read_value = 0;
  if(read_string.startsWith("v")) {
    read_value = read_string.substring(1).toInt();

    if(read_value <= 255 && read_value >= 0) {
      duty_cycle = read_value;
      analogWrite(pin, duty_cycle);
      Serial.write(String("updated duty cycle: ") + String(duty_cycle));
    }
  }
}
