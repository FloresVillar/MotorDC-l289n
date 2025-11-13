import numpy as np 
import sys
### CONECTAR ARDUINO
 
import tkinter as tk
def click_boton_label():
    print("BOTON CLICKEADO")
    
def tkinter_ventana_principal_clase5():
    print(tk.TkVersion)
    ventana = tk.Tk()
    ventana.title("Titulo")
    ventana.geometry("600x400")
    ventana.update_idletasks()
    #ventana.mainloop()  muestra
    label = tk.Label(ventana, text = "LABEL")
    label.place(relx= 0.5, rely = 0.25, anchor = "n") #posicionamiento relativo
    #ventana.mainloop()
    #ventana.mainloop()                              #                                w   center e
    texto = tk.Entry(ventana, width = 10,fg ="blue", font=("Arial",8)) 
    texto.place(relx =0.5,rely=0.5,anchor = "center" )                                 #sw  s     se          
    #ventana.mainloop()
    def clickeado():
        res = "Usted escribio : " + texto.get()
        label.configure(text = res)
    boton = tk.Button(ventana, text = "CLICK", command = clickeado,fg = "white",bg = "green",width = 15, height = 2) #width cantidad de caracteres, heinght cantidad de lineas
    boton.place(relx=0.5,rely=0.85,anchor ="s") #el centro del boton se ubica en (x,y) nw     n   ne
    ventana.mainloop()

def sliders_clase6():
    ventana = tk.Tk()
    ventana.title("sliders")
    ventana.geometry("500x500")
    def actualizar_color(valor):
        v_int = int(float(valor))
        c_hex = f'#{v_int:02x}{v_int:02x}{v_int:02x}'
        ventana.configure(bg=c_hex)
    vertical_slider = tk.Scale(ventana,from_=0,to_=180,orient=tk.HORIZONTAL,label="slider horizontal",length = 200,command = actualizar_color)
    vertical_slider.place(relx=0,rely=0,anchor="nw")
    ventana.mainloop()

import serial
import time

v_actual = 0
intensidad_f = 100

def actualizar_valor(val):  
        global v_actual, intensidad_f
        v_actual = int(val)
        if v_actual > 0:
            boton_apagar.config(text = "Apagar LED")
            intensidad_f = v_actual
        else:
            boton_apagar.config(text = "Encender LED")

def palanca_led():
    global v_actual, intensidad_f
    if v_actual > 0:
            intesidad_f = v_actual
            v_actual = 0
            slider.set(0)
            boton_apagar.config(text = "Encender LED")
    else:
        v_actual = intensidad_f
        slider.set(intensidad_f)
        boton_apagar.config(text = "Apagar LED")

def enviar_constante():
    try:
        arduino.write(f"{v_actual}\n".encode())
    except:
        print("ERROR AL ENVIAR A ARDUINO")
    ventana.after(200,enviar_constante)

def ejercicio3_clase6():
    global slider, boton_apagar, ventana, arduino
    arduino = serial.Serial('COM3',9600)
    time.sleep(2) 
    ventana = tk.Tk()
    ventana.title("ARDUINO")
    ventana.geometry("500x500")
    slider = tk.Scale(ventana, from_ = 0, to_ = 255 , length = 300, bg = "lightblue", orient = tk.HORIZONTAL, label = "intensidad LED",command = actualizar_valor)
    slider.set(0)
    slider.place(relx=0,rely=0,anchor="nw")
    boton_apagar = tk.Button(ventana, text = "Encender LED", command = palanca_led, bg = "red", fg = "white")
    boton_apagar.place(relx = 0.5,rely = 1, anchor = "s")
    ventana.configure(bg = 'lightblue')
    ventana.after(200,enviar_constante)
    ventana.mainloop()
    arduino.close()
        
    
if __name__=='__main__':
    #ejercicio1()
    #ejercicio2()
    #ejercicio3()
    #ejercicio4()
    #ejercicio1_clase2()
    #ejercicio2_clase2()
    #ejercicio3_clase2()
    #ejercicio4_clase2()
    #ejercicio5_clase2()
    #tkinter_ventana_principal_clase5()
    #sliders_clase6()
    #tkinter_ventana_principal_clase5()
    sliders_clase6()