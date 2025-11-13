# PC3 Control inteligente de velocidad de motor

**Grupo 1** 
- Control inteligente de velocidad de motor Conecta un motor DC con un módulo L298N al Arduino. Implementa una interfaz con Tkinter que: 
-  Permita ajustar la velocidad del motor mediante un Scale (PWM de 0–255). 
-  Muestre la velocidad actual en porcentaje. 
-  Incluya un botón de inicio y parada que detenga inmediatamente el motor. 
-  Si el usuario mantiene el motor a más del 80% de velocidad durante más de 10 segundos, muestra una alerta visual (roja) en la interfaz. 
- Integre un gráfico de evolución de velocidad vs. tiempo

L298n es un modulo para manejar motores , sera el puente entre el motor que requiere potencia y el arduino , quien trabaja con voltajes menores.

```bash  
            MÓDULO L298N  
           
        +---------------------------------------+
        |       Disipador negro                 |
MOTOR1  |                                       |         MOTOR2
OUT1+   |⟷                                   ⟷| OUT3   → -
OUT2-   |⟷                                   ⟷| OUT4  →  +
        |---------------------------------------|
        |         |                             |
        |   [J jumper]                          |
        +12V  GND  +5V ENA IN1 IN2 IN3 IN4 ENB 
        +--------------------------------------+
                       ↑ Control (Arduino)
```
Se usara el MOTOR 1 luego se conectara estos bordes de potencia(CAJAS AZULES) al motor DC en cuestión OUT1 y OUT2.En este caso los cables de nuestro motor no tiene polaridad fija entonces los conectamos de forma indistinta. 
Seguidamente la entrada EN1 se conecta al pin 7 del arduino, para  luego hacer lo propio entre la entrada EN2 y el  pin 6 del arduino. De modo que  :
```bash
PIN 6 =1 →→ IN1 = 1 →→ OUT1 =6V 
PIN 7 =0 →→ IN2 = 0 →→ OUT2=GND=0
#obtenemos el giro en un sentido
PIN 6=0 →→  IN1=0  →→  OUT1=GND
PIN 7 =1 →→ IN2=1  →→ OUT2=6V
#obtenemos el giro contrario
```
Ademas si se quiere variar la velocidad conectamos el pin 5 del arudino al jumper ENA de activacion para el MOTOR1

La bateria por su parte se conecta a los bordes de potencia (CAJAS AZULES) 12V(+) y GND(- referencia electrica "tierra") respectivamente.
Ahora bien como se va a medir potencias tanto arduino como L289n deben tener la misma referencia desde el cual medir dicho voltaje, luego se conecta tanto el negativo de la bateria como el GND del arduino al  GND del l289n.