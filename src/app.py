import eel
import json
import os
import sys
import psutil
import winreg
import keyboard
import tkinter as tk
from tkinter import filedialog

# --- Rutas ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

# Inicializar Eel
eel.init('web')

# --- LÓGICA DE BÚSQUEDA (Igual que antes) ---
def buscar_navegadores_sistema():
    encontrados = []
    rutas_vistas = set()

    # 1. Registro
    rutas_reg = [
        r"SOFTWARE\Clients\StartMenuInternet",
        r"SOFTWARE\WOW6432Node\Clients\StartMenuInternet"
    ]
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

    # 2. Búsqueda Manual AppData
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

# --- API EEL ---

@eel.expose
def get_data_inicial():
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f: config = json.load(f)
        except: pass
    return {"config": config, "sistema": buscar_navegadores_sistema()}

@eel.expose
def grabar_atajo():
    return keyboard.read_hotkey(suppress=False)

@eel.expose
def examinar_exe():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    ruta = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
    root.destroy()
    if ruta:
        return {"nombre": os.path.basename(ruta).replace(".exe", "").capitalize(), "ruta": ruta}
    return None

@eel.expose
def guardar_configuracion(atajo, lista_activos):
    data = {"atajo": atajo, "navegadores_activos": lista_activos, "indice_actual": 0}
    try:
        with open(CONFIG_FILE, 'w') as f: json.dump(data, f, indent=4)
        reiniciar_controlador()
        return True
    except Exception as e: return str(e)

def reiniciar_controlador():
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

# Arrancar Eel
eel.start('index.html', size=(700, 500), port=0)