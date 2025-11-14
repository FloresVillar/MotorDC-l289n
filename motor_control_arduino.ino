
const int pwma = 9;   // PWM pin (PWMA)
const int ain1 = 8;   // AIN1
const int ain2 = 7;   // AIN2
const int stby = 6;   // STBY (enable for TB6612)

void setup() {
  Serial.begin(9600);
  pinMode(pwma, OUTPUT);
  pinMode(ain1, OUTPUT);
  pinMode(ain2, OUTPUT);
  pinMode(stby, OUTPUT);

  // Enable driver (exit standby)
  digitalWrite(stby, HIGH);

  // Default direction: forward (AIN1 HIGH, AIN2 LOW)
  digitalWrite(ain1, HIGH);
  digitalWrite(ain2, LOW);
  analogWrite(pwma, 0);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.length() == 0) return;

    if (line.startsWith("S:")) {
      int val = line.substring(2).toInt();
      val = constrain(val, 0, 255);
      analogWrite(pwma, val);
      Serial.print("OK S:");
      Serial.println(val);
    } else if (line.equalsIgnoreCase("STOP")) {
      analogWrite(pwma, 0);
      Serial.println("OK STOP");
    } else if (line.equalsIgnoreCase("EMERGENCY_STOP")) {
      // hard stop: disable driver by pulling STBY LOW (puts TB6612 in standby)
      analogWrite(pwma, 0);
      digitalWrite(ain1, LOW);
      digitalWrite(ain2, LOW);
      digitalWrite(stby, LOW);
      Serial.println("OK EMERGENCY_STOP (STBY LOW)");
    }
  }
}
