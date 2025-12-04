import sys
import os
import subprocess
import json

# --- Configuración de Rutas ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def abrir_url(url):
    config = cargar_config()
    
    # Fallback si no hay config
    if not config or not config.get("navegadores_activos"):
        os.system(f'start chrome "{url}"')
        return

    # Obtener el navegador que toca según el índice actual
    idx = config.get("indice_actual", 0)
    lista = config.get("navegadores_activos", [])
    
    # Asegurar que el índice es válido
    if idx >= len(lista): idx = 0
    
    navegador_data = lista[idx]
    ruta_exe = navegador_data["ruta"]

    try:
        subprocess.Popen([ruta_exe, url])
    except Exception as e:
        # Si falla la ruta específica, intentamos abrir por nombre (menos fiable pero útil)
        os.system(f'start {navegador_data["nombre"]} "{url}"')

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.google.com"
    abrir_url(url)