int motorPin = 5;   // ENA → PWM
int in1 = 6;        // IN1
int in2 = 7;        // IN2

int velocidad = 0;  // PWM actual
bool motorEncendido = false;

void setup() {
  pinMode(motorPin, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  Serial.begin(9600);
}

// Función para actualizar dirección y velocidad
void actualizarMotor(int pwm, bool encendido) {
  if(encendido){
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);    // Giro en un sentido
    analogWrite(motorPin, pwm); // PWM controla velocidad
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);    // Motor detenido
    analogWrite(motorPin, 0);  // Asegura apagado
  }
}

void loop() {
  if(Serial.available()){
    // Recibimos: "<valorPWM>,<encendido>"
    String datos = Serial.readStringUntil('\n');
    int coma = datos.indexOf(',');
    if(coma > 0){
      int pwm = datos.substring(0,coma).toInt();
      int enc = datos.substring(coma+1).toInt();
      motorEncendido = (enc == 1);
      actualizarMotor(pwm, motorEncendido);
    }
  }
}
