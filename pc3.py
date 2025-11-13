import numpy as np
import tkinter as tk 
import sys
import serial
import time

v_actual = 0 #PWD modulacion por ancho de pulso

arduino = serial.Serial('COM4',9600)
time.sleep(2)

def modificacion_velocidad_PWM():
    def actualizar_valor(val):
        global v_actual 
        v_actual = int(val)
        try:
            arduino.write(f"{v_actual}\n".encode())
        except:
            print("Error al enviar a Arduino")
    ventana = tk.Tk()
    ventana.title("control de velocidad")
    ventana.geometry("500x500")
    horizontal_slider = tk.Scale(ventana,from_=0,to_=255,orient=tk.HORIZONTAL,label="slider horizontal",length = 200,command = actualizar_valor)
    horizontal_slider.place(relx=0,rely=0,anchor="nw")
    ventana.mainloop()  
    arduino.close()

if __name__=='__main__':
    modificacion_velocidad_PWM()