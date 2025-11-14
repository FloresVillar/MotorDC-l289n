import tkinter as tk
import serial
import time

v_actual = 0
motor_encendido = False

class MockSerial:
    def __init__(self, port, baudrate):
        print(f"Simulando conexión serial en {port} a {baudrate} baudios")

    def write(self, data):
        print(f"Enviando datos simulados: {data.decode().strip()}")

    def close(self):
        print("Cerrando conexión simulada")

# Reemplazar arduino = serial.Serial(...) por:
arduino = MockSerial('COM4', 9600)
#arduino = serial.Serial('COM4',9600)
time.sleep(2)

def actualizar_valor(val):
    global v_actual
    v_actual = int(val)
    try:
    # Enviamos "<PWM>,<Encendido>" como cadena
        arduino.write(f"{v_actual},{int(motor_encendido)}\n".encode())
    except:
        print("Error al enviar a Arduino")

def palanca_motor():
    global motor_encendido
    motor_encendido = not motor_encendido
    if motor_encendido:
        boton_apagar.config(text="Apagar Motor")
    else:
        boton_apagar.config(text="Encender Motor")
    try:
        # Enviamos "<PWM>,<Encendido>" como cadena
        arduino.write(f"{v_actual},{int(motor_encendido)}\n".encode())
    except:
        print("Error al enviar a Arduino")
    

# Tkinter
ventana = tk.Tk()
ventana.title("Control de velocidad motor")
ventana.geometry("500x300")

slider = tk.Scale(ventana, from_=0, to_=255, orient=tk.HORIZONTAL,
                  label="Velocidad motor (PWM)", length=300,
                  command=actualizar_valor)
slider.place(relx=0.5, rely=0.3, anchor="center")

boton_apagar = tk.Button(ventana, text="Encender Motor", command=palanca_motor,
                         bg="red", fg="white", width=15, height=2)
boton_apagar.place(relx=0.5, rely=0.7, anchor="center")

ventana.mainloop()
arduino.close()
