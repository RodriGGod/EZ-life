import sys
import os
import subprocess

# --- Configuración de Rutas ---
if getattr(sys, 'frozen', False):
    CARPETA_BASE = os.path.dirname(sys.executable)
else:
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_ESTADO = os.path.join(CARPETA_BASE, 'estado.txt')
ARCHIVO_LOG = os.path.join(CARPETA_BASE, 'debug_log.txt')

# --- RUTAS DE NAVEGADORES (VERIFICA ESTAS RUTAS EN TU PC) ---
# A veces Brave se instala en Local AppData en lugar de Archivos de Programa
user_path = os.path.expanduser("~")

PATH_OPERA = os.path.join(user_path, r"AppData\Local\Programs\Opera GX\launcher.exe")
PATH_BRAVE_1 = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
PATH_BRAVE_2 = os.path.join(user_path, r"AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")

def log(mensaje):
    """Escribe errores en un archivo de texto para poder leerlos"""
    try:
        with open(ARCHIVO_LOG, 'a') as f:
            f.write(f"{mensaje}\n")
    except:
        pass

def leer_estado():
    try:
        if os.path.exists(ARCHIVO_ESTADO):
            with open(ARCHIVO_ESTADO, 'r') as f:
                return f.read().strip()
        else:
            log("No se encontró estado.txt, usando default.")
            return "brave"
    except Exception as e:
        log(f"Error leyendo estado: {e}")
        return "brave"

def abrir_url(url):
    navegador = leer_estado()
    log(f"Intentando abrir: {navegador} con url: {url}")
    
    ejecutable = None

    if navegador == "opera":
        if os.path.exists(PATH_OPERA):
            ejecutable = PATH_OPERA
        else:
            log(f"No encuentro Opera en: {PATH_OPERA}")

    elif navegador == "brave":
        if os.path.exists(PATH_BRAVE_1):
            ejecutable = PATH_BRAVE_1
        elif os.path.exists(PATH_BRAVE_2):
            ejecutable = PATH_BRAVE_2
        else:
            log(f"No encuentro Brave en ProgramFiles ni AppData")

    # Intentar abrir
    if ejecutable:
        try:
            subprocess.Popen([ejecutable, url])
        except Exception as e:
            log(f"Fallo subprocess: {e}")
    else:
        # Fallback de emergencia
        log("Usando fallback de sistema (start browser)")
        os.system(f'start {navegador} "{url}"')

if __name__ == '__main__':
    url_objetivo = "https://www.google.com"
    if len(sys.argv) > 1:
        url_objetivo = sys.argv[1]
    
    abrir_url(url_objetivo)