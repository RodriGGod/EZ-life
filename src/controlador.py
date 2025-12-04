import keyboard
import os
import sys
import json
import threading
import tkinter as tk
import time

# --- Rutas ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def guardar_indice(nuevo_indice):
    # Leemos, modificamos solo el índice y guardamos
    try:
        with open(CONFIG_FILE, 'r+') as f:
            data = json.load(f)
            data["indice_actual"] = nuevo_indice
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception as e:
        print(f"Error guardando: {e}")

# --- GUI del Tooltip (Mensajito) ---
def mostrar_tooltip(texto):
    def _run():
        try:
            root = tk.Tk()
            root.overrideredirect(True)
            root.attributes("-topmost", True)
            # Color aleatorio o fijo según quieras. Usaremos gris oscuro elegante.
            lbl = tk.Label(root, text=texto, bg="#333333", fg="#00ff00", 
                           font=("Segoe UI", 10, "bold"), padx=15, pady=8)
            lbl.pack()
            
            # Posición ratón
            x, y = root.winfo_pointerx(), root.winfo_pointery()
            root.geometry(f"+{x+20}+{y+20}")
            
            root.after(1200, root.destroy)
            root.mainloop()
        except: pass
    threading.Thread(target=_run, daemon=True).start()

def cambiar_navegador():
    config = cargar_config()
    if not config: return

    lista = config.get("navegadores_activos", [])
    if not lista: return

    # Calcular siguiente índice
    idx_actual = config.get("indice_actual", 0)
    nuevo_idx = (idx_actual + 1) % len(lista) # Rotación circular
    
    guardar_indice(nuevo_idx)
    
    # Feedback visual
    nombre_nuevo = lista[nuevo_idx]["nombre"]
    mostrar_tooltip(f"🌍 Cambiado a: {nombre_nuevo}")

# --- Main Loop ---
def main():
    print("Iniciando Controlador...")
    config = cargar_config()
    
    if config and config.get("atajo"):
        atajo = config["atajo"]
        print(f"Escuchando atajo: {atajo}")
        try:
            keyboard.add_hotkey(atajo, cambiar_navegador)
            keyboard.wait()
        except Exception as e:
            print(f"Error en el atajo: {e}")
            time.sleep(5) # Evitar cierre inmediato si falla
    else:
        print("No hay configuración válida. Ejecuta la App primero.")

if __name__ == "__main__":
    main()