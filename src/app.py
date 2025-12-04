import webview
import json
import os
import sys
import psutil
import winreg
import keyboard
import tkinter as tk
from tkinter import filedialog
import threading

# --- Rutas ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
WEB_DIR = os.path.join(BASE_DIR, 'web')

# --- CLASE API (Lo que antes eran funciones @eel.expose) ---
class Api:
    def get_data_inicial(self):
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f: config = json.load(f)
            except: pass
        return {"config": config, "sistema": self.buscar_navegadores_sistema()}

    def grabar_atajo(self):
        # pywebview puede bloquearse si no usamos threads para input bloqueante
        return keyboard.read_hotkey(suppress=False)

    def examinar_exe(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        ruta = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        root.destroy()
        if ruta:
            return {"nombre": os.path.basename(ruta).replace(".exe", "").capitalize(), "ruta": ruta}
        return None

    def guardar_configuracion(self, atajo, lista_activos):
        data = {"atajo": atajo, "navegadores_activos": lista_activos, "indice_actual": 0}
        try:
            with open(CONFIG_FILE, 'w') as f: json.dump(data, f, indent=4)
            self.reiniciar_controlador()
            return True
        except Exception as e: return str(e)

    def cerrar_app(self):
        # Función para el botón X personalizado
        os._exit(0)

    # --- LÓGICA INTERNA ---
    def buscar_navegadores_sistema(self):
        # (Misma lógica que tenías antes)
        encontrados = []
        rutas_vistas = set()
        rutas_reg = [r"SOFTWARE\Clients\StartMenuInternet", r"SOFTWARE\WOW6432Node\Clients\StartMenuInternet"]
        roots = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

        for root in roots:
            for sub_reg in rutas_reg:
                try:
                    key = winreg.OpenKey(root, sub_reg)
                    count = winreg.QueryInfoKey(key)[0]
                    for i in range(count):
                        try:
                            name = winreg.EnumKey(key, i)
                            cmd_path = sub_reg + "\\" + name + "\\shell\\open\\command"
                            cmd_key = winreg.OpenKey(root, cmd_path)
                            val, _ = winreg.QueryValueEx(cmd_key, "")
                            exe_path = val.replace('"', '').strip()
                            if os.path.exists(exe_path) and exe_path not in rutas_vistas:
                                display_name = name
                                if "Opera GX" in name or "OperaGX" in exe_path: display_name = "Opera GX"
                                if "Brave" in name: display_name = "Brave Browser"
                                encontrados.append({"nombre": display_name, "ruta": exe_path})
                                rutas_vistas.add(exe_path)
                        except: continue
                except: continue
        
        # Manual AppData
        user_home = os.path.expanduser("~")
        rutas_extra = [
            (os.path.join(user_home, r"AppData\Local\Programs\Opera GX\launcher.exe"), "Opera GX"),
            (os.path.join(user_home, r"AppData\Local\Programs\Opera\launcher.exe"), "Opera"),
            (r"C:\Program Files\Opera GX\launcher.exe", "Opera GX")
        ]
        for path, name in rutas_extra:
            if os.path.exists(path) and path not in rutas_vistas:
                encontrados.append({"nombre": name, "ruta": path})
                rutas_vistas.add(path)
        return encontrados

    def reiniciar_controlador(self):
        nombre = "controlador.exe"
        for proc in psutil.process_iter():
            try:
                if proc.name() == nombre: proc.kill()
            except: pass
        ruta = os.path.join(BASE_DIR, nombre)
        if os.path.exists(ruta): os.startfile(ruta)
        else:
            ruta_dev = os.path.join(BASE_DIR, "controlador.py")
            if os.path.exists(ruta_dev): os.system(f'start python "{ruta_dev}"')

# --- INICIO DE VENTANA ---
if __name__ == '__main__':
    api = Api()
    # AQUÍ ESTÁ LA MAGIA: frameless=True, transparent=True
    window = webview.create_window(
        'EZLife Tool', 
        url=os.path.join(WEB_DIR, 'index.html'),
        js_api=api,
        width=720, height=520,
        frameless=True,      # Quita bordes de Windows
        transparent=True,    # Activa transparencia real
        easy_drag=True       # Allow dragging from anywhere
    )
    webview.start(debug=False)