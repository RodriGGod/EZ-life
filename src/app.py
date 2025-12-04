import webview
import json
import os
import sys
import psutil
import winreg
import keyboard
import tkinter as tk
from tkinter import filedialog


# --- 1. CONFIGURACIÓN DE RUTAS (CRÍTICO PARA EVITAR ERROR 404) ---
if getattr(sys, 'frozen', False):
    # SI ESTAMOS EN MODO .EXE (Instalado)
    # sys._MEIPASS es la carpeta temporal donde PyInstaller descomprime los archivos
    BASE_DIR = sys._MEIPASS
    # La configuración la guardamos en APPDATA para tener permisos de escritura
    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'EZLifeTool')
else:
    # SI ESTAMOS EN MODO DESARROLLO (python app.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'EZLifeTool')

# Definimos dónde está la carpeta web y el archivo de configuración
WEB_DIR = os.path.join(BASE_DIR, 'web')
CONFIG_FILE = os.path.join(APP_DATA_DIR, 'config.json')

# Crear carpeta en AppData si no existe
if not os.path.exists(APP_DATA_DIR):
    try:
        os.makedirs(APP_DATA_DIR)
    except:
        pass

# --- 2. CLASE API (PUENTE ENTRE JAVASCRIPT Y PYTHON) ---
class Api:
    def get_data_inicial(self):
        """Lee la configuración y busca navegadores al iniciar"""
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except:
                pass
        
        # Calcular ruta del Browser
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
            
        browser_path = os.path.join(base_path, 'EZLife_Browser.exe')
        if not os.path.exists(browser_path):
            browser_path = "EZLife_Browser.exe not found (Build it first!)"

        return {"config": config, "sistema": self.buscar_navegadores_sistema(), "browserPath": browser_path}

    def grabar_atajo(self):
        """Escucha el teclado (bloqueante, por eso se llama con timeout desde JS)"""
        return keyboard.read_hotkey(suppress=False)

    def examinar_exe(self):
        """Abre el explorador de archivos de Windows"""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        ruta = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        root.destroy()
        if ruta:
            nombre = os.path.basename(ruta).replace(".exe", "").capitalize()
            return {"nombre": nombre, "ruta": ruta}
        return None

    def guardar_configuracion(self, atajo, lista_activos):
        """Guarda el JSON y reinicia el controlador invisible"""
        data = {
            "atajo": atajo,
            "navegadores_activos": lista_activos,
            "indice_actual": 0
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            self.reiniciar_controlador()
            return True
        except Exception as e:
            return str(e)

    def cerrar_app(self):
        """Cierra la aplicación completamente"""
        os._exit(0)

    def open_default_apps(self):
        """Abre la configuración de aplicaciones predeterminadas de Windows"""
        os.system('start ms-settings:defaultapps')

    # --- Lógica Interna del Sistema ---
    def buscar_navegadores_sistema(self):
        encontrados = []
        rutas_vistas = set()
        
        # 1. Buscar en Registro de Windows
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

        # 2. Buscar Manualmente en AppData (Común para Opera GX)
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
        nombre_proceso = "controlador.exe"
        # 1. Matar proceso existente
        for proc in psutil.process_iter():
            try:
                if proc.name() == nombre_proceso:
                    proc.kill()
            except: pass
        
        # 2. Iniciar nuevo proceso
        if getattr(sys, 'frozen', False):
            # Si estamos instalados, el controlador está en la misma carpeta que este exe
            INSTALL_DIR = os.path.dirname(sys.executable)
            ruta = os.path.join(INSTALL_DIR, nombre_proceso)
        else:
            # Si estamos en desarrollo
            ruta = os.path.join(BASE_DIR, "controlador.py")

        if os.path.exists(ruta):
            os.startfile(ruta)
        elif os.path.exists(ruta.replace(".exe", ".py")):
            os.system(f'start python "{ruta}"')

# --- 3. INICIO DE LA VENTANA ---
if __name__ == '__main__':
    api = Api()
    
    # Comprobación de seguridad: ¿Existe el index.html?
    archivo_html = os.path.join(WEB_DIR, 'index.html')
    if not os.path.exists(archivo_html):
        # Si esto sale, es que PyInstaller no copió la carpeta web
        print(f"ERROR FATAL: No encuentro el archivo: {archivo_html}")
        # En modo ventana no verás este print, pero es útil si depuras
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

# --- 1. CONFIGURACIÓN DE RUTAS (CRÍTICO PARA EVITAR ERROR 404) ---
if getattr(sys, 'frozen', False):
    # SI ESTAMOS EN MODO .EXE (Instalado)
    # sys._MEIPASS es la carpeta temporal donde PyInstaller descomprime los archivos
    BASE_DIR = sys._MEIPASS
    # La configuración la guardamos en APPDATA para tener permisos de escritura
    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'EZLifeTool')
else:
    # SI ESTAMOS EN MODO DESARROLLO (python app.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'EZLifeTool')

# Definimos dónde está la carpeta web y el archivo de configuración
WEB_DIR = os.path.join(BASE_DIR, 'web')
CONFIG_FILE = os.path.join(APP_DATA_DIR, 'config.json')

# Crear carpeta en AppData si no existe
if not os.path.exists(APP_DATA_DIR):
    try:
        os.makedirs(APP_DATA_DIR)
    except:
        pass

# --- 2. CLASE API (PUENTE ENTRE JAVASCRIPT Y PYTHON) ---
class Api:
    def get_data_inicial(self):
        """Lee la configuración y busca navegadores al iniciar"""
        config = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except:
                pass
        
        # Calcular ruta del Browser
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
            
        browser_path = os.path.join(base_path, 'EZLife_Browser.exe')
        if not os.path.exists(browser_path):
            browser_path = "EZLife_Browser.exe not found (Build it first!)"

        return {"config": config, "sistema": self.buscar_navegadores_sistema(), "browserPath": browser_path}

    def grabar_atajo(self):
        """Escucha el teclado (bloqueante, por eso se llama con timeout desde JS)"""
        return keyboard.read_hotkey(suppress=False)

    def examinar_exe(self):
        """Abre el explorador de archivos de Windows"""
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        ruta = filedialog.askopenfilename(filetypes=[("Ejecutables", "*.exe")])
        root.destroy()
        if ruta:
            nombre = os.path.basename(ruta).replace(".exe", "").capitalize()
            return {"nombre": nombre, "ruta": ruta}
        return None

    def guardar_configuracion(self, atajo, lista_activos):
        """Guarda el JSON y reinicia el controlador invisible"""
        data = {
            "atajo": atajo,
            "navegadores_activos": lista_activos,
            "indice_actual": 0
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            self.reiniciar_controlador()
            return True
        except Exception as e:
            return str(e)

    def cerrar_app(self):
        """Cierra la aplicación completamente"""
        os._exit(0)

    def open_default_apps(self):
        """Abre la configuración de aplicaciones predeterminadas de Windows"""
        os.system('start ms-settings:defaultapps')

    # --- Lógica Interna del Sistema ---
    def buscar_navegadores_sistema(self):
        encontrados = []
        rutas_vistas = set()
        
        # 1. Buscar en Registro de Windows
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

        # 2. Buscar Manualmente en AppData (Común para Opera GX)
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
        nombre_proceso = "controlador.exe"
        # 1. Matar proceso existente
        for proc in psutil.process_iter():
            try:
                if proc.name() == nombre_proceso:
                    proc.kill()
            except: pass
        
        # 2. Iniciar nuevo proceso
        if getattr(sys, 'frozen', False):
            # Si estamos instalados, el controlador está en la misma carpeta que este exe
            INSTALL_DIR = os.path.dirname(sys.executable)
            ruta = os.path.join(INSTALL_DIR, nombre_proceso)
        else:
            # Si estamos en desarrollo
            ruta = os.path.join(BASE_DIR, "controlador.py")

        if os.path.exists(ruta):
            os.startfile(ruta)
        elif os.path.exists(ruta.replace(".exe", ".py")):
            os.system(f'start python "{ruta}"')

# --- 3. INICIO DE LA VENTANA ---
if __name__ == '__main__':
    api = Api()
    
    # Comprobación de seguridad: ¿Existe el index.html?
    archivo_html = os.path.join(WEB_DIR, 'index.html')
    if not os.path.exists(archivo_html):
        # Si esto sale, es que PyInstaller no copió la carpeta web
        print(f"ERROR FATAL: No encuentro el archivo: {archivo_html}")
        # En modo ventana no verás este print, pero es útil si depuras
    
    window = webview.create_window(
        'EZLife Tool', 
        url=archivo_html,  # Usamos la ruta absoluta calculada
        js_api=api,
        width=720, height=520,
        frameless=True,      
        transparent=True,    
        easy_drag=True,
        resizable=True
    )
    webview.start(debug=False)