import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import collections

import serial
import serial.tools.list_ports

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PWM_MAX = 255
ALERT_PERCENT_THRESHOLD = 80 
ALERT_SECONDS = 10.0
PLOT_WINDOW_SECONDS = 60  

class MotorControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control inteligente de velocidad de motor - Grupo 1")

        self.serial_port = None
        self.ser_lock = threading.Lock()
        self.motor_running = False
        self.last_sent_value = 0

        self.alert_active = False
        self.high_speed_start = None
        self.run_start = time.time()

        self.times = collections.deque()
        self.speeds = collections.deque()

        self._build_ui()
        self._start_periodic_update()

    def _build_ui(self):
        frm_top = ttk.Frame(self.root)
        frm_top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        # Serial port selection
        ttk.Label(frm_top, text="COM: ").pack(side=tk.LEFT)
        self.combobox = ttk.Combobox(frm_top, values=self._list_serial_ports(), width=12)
        self.combobox.pack(side=tk.LEFT)
        self.combobox.set(self.combobox['values'][0] if self.combobox['values'] else '')
        ttk.Button(frm_top, text="Conectar", command=self.connect_serial).pack(side=tk.LEFT, padx=(6,0))
        ttk.Button(frm_top, text="Refrescar puertos", command=self._refresh_ports).pack(side=tk.LEFT, padx=(6,0))

        # Scale and percent
        frm_ctrl = ttk.Frame(self.root)
        frm_ctrl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        ttk.Label(frm_ctrl, text="Velocidad (PWM 0-255):").pack(anchor=tk.W)
        self.scale = tk.Scale(frm_ctrl, from_=0, to=PWM_MAX, orient=tk.HORIZONTAL, length=400, command=self._on_scale)
        self.scale.pack()

        self.percent_label = ttk.Label(frm_ctrl, text="0 %")
        self.percent_label.pack(anchor=tk.W)

        # Start / Stop buttons
        frm_buttons = ttk.Frame(self.root)
        frm_buttons.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        self.start_btn = ttk.Button(frm_buttons, text="Inicio", command=self.start_motor)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = ttk.Button(frm_buttons, text="Parar", command=self.stop_motor)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        self.emer_stop_btn = ttk.Button(frm_buttons, text="Parada INMEDIATA", command=self.emergency_stop)
        self.emer_stop_btn.pack(side=tk.LEFT, padx=12)

        # Alert label
        self.alert_label = tk.Label(self.root, text="", bg=self.root.cget('bg'), fg='white')
        self.alert_label.pack(fill=tk.X, padx=8, pady=(4,0))

        # Matplotlib figure
        self.fig = Figure(figsize=(6,3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Velocidad vs Tiempo')
        self.ax.set_xlabel('s')
        self.ax.set_ylabel('%')
        self.line, = self.ax.plot([], [], '-b')
        self.ax.set_ylim(0, 105)

        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=6)
        self.canvas = canvas

    def _list_serial_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return ports

    def _refresh_ports(self):
        self.combobox['values'] = self._list_serial_ports()

    def connect_serial(self):
        port = self.combobox.get().strip()
        if not port:
            messagebox.showwarning('Puerto COM', 'Seleccione un puerto COM válido')
            return
        try:
            with self.ser_lock:
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.close()
                self.serial_port = serial.Serial(port, 9600, timeout=0.1)
            messagebox.showinfo('Conectado', f'Conectado a {port} (9600)')
        except Exception as e:
            messagebox.showerror('Error conexión', str(e))
            self.serial_port = None

    def send_serial(self, msg: str):
        # Non-blocking wrapper
        try:
            with self.ser_lock:
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.write((msg + '\n').encode('utf-8'))
                    return True
        except Exception as e:
            print('Serial write error:', e)
        return False

    def _on_scale(self, val):
        val = int(float(val))
        percent = int(round(val / PWM_MAX * 100))
        self.percent_label.config(text=f"{percent} %")
        if self.motor_running:
            self._send_speed(val)
        self.last_sent_value = val

    def start_motor(self):
        val = int(self.scale.get())
        self.motor_running = True
        self._send_speed(val)
        if not self.times:
            self.run_start = time.time()

    def stop_motor(self):
        self.motor_running = False
        self._send_stop()
        # keep scale value, but set last_sent to 0
        self.last_sent_value = 0

    def emergency_stop(self):
        self.motor_running = False
        # emergency stop command for Arduino
        self.send_serial('EMERGENCY_STOP')
        # also send STOP for compatibility
        self._send_stop()
        self.scale.set(0)
        self.last_sent_value = 0

    def _send_speed(self, pwm_value: int):
        pwm_value = max(0, min(PWM_MAX, int(pwm_value)))
        self.send_serial(f'S:{pwm_value}')
        self.last_sent_value = pwm_value

    def _send_stop(self):
        self.send_serial('STOP')

    def _start_periodic_update(self):
        self._update_loop()

    def _update_loop(self):
        # Called by Tkinter via after
        now = time.time()
        elapsed = now - self.run_start

        percent = int(round(self.last_sent_value / PWM_MAX * 100))
        self.times.append(elapsed)
        self.speeds.append(percent)

        while self.times and (self.times[-1] - self.times[0]) > PLOT_WINDOW_SECONDS:
            self.times.popleft()
            self.speeds.popleft()

        if self.times:
            self.line.set_data(list(self.times), list(self.speeds))
            self.ax.set_xlim(max(0, self.times[0]), max(PLOT_WINDOW_SECONDS, self.times[-1]))
        else:
            self.line.set_data([], [])
            self.ax.set_xlim(0, PLOT_WINDOW_SECONDS)
        self.canvas.draw_idle()

        if percent >= ALERT_PERCENT_THRESHOLD:
            if self.high_speed_start is None:
                self.high_speed_start = now
            else:
                if (now - self.high_speed_start) >= ALERT_SECONDS and not self.alert_active:
                    self._activate_alert()
        else:
            self.high_speed_start = None
            if self.alert_active:
                self._clear_alert()

        self.root.after(500, self._update_loop)

    def _activate_alert(self):
        self.alert_active = True
        self.alert_label.config(text=f"ALERTA: velocidad > {ALERT_PERCENT_THRESHOLD}% por más de {int(ALERT_SECONDS)} s", bg='red')

    def _clear_alert(self):
        self.alert_active = False
        self.alert_label.config(text='', bg=self.root.cget('bg'))


if __name__ == '__main__':
    root = tk.Tk()
    app = MotorControllerApp(root)
    root.mainloop()
