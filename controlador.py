import keyboard
import os
import sys
import threading
import tkinter as tk

# --- Configuración de Rutas ---
if getattr(sys, 'frozen', False):
    CARPETA_BASE = os.path.dirname(sys.executable)
else:
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_ESTADO = os.path.join(CARPETA_BASE, 'estado.txt')

def leer_estado_actual():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, 'r') as f:
            return f.read().strip()
    return "brave"

def guardar_estado(navegador):
    try:
        with open(ARCHIVO_ESTADO, 'w') as f:
            f.write(navegador)
    except:
        pass

# --- Función para mostrar el mensaje visual ---
def mostrar_tooltip(texto, color_fondo):
    """Crea una mini ventana flotante en la posición del ratón"""
    
    def _run_gui():
        try:
            root = tk.Tk()
            root.overrideredirect(True) # Quitar bordes y barra de título
            root.attributes("-topmost", True) # Mantener siempre visible encima de todo
            
            # Configuración de estilo
            label = tk.Label(root, text=texto, bg=color_fondo, fg="white", 
                             font=("Arial", 10, "bold"), padx=10, pady=5)
            label.pack()

            # Obtener posición del ratón
            x = root.winfo_pointerx()
            y = root.winfo_pointery()
            
            # Posicionar la ventanita un poco a la derecha del ratón
            root.geometry(f"+{x+15}+{y+15}")

            # Cerrar automáticamente después de 1 segundo (1000 ms)
            root.after(1000, root.destroy)
            root.mainloop()
        except:
            pass

    # Ejecutamos la interfaz en un hilo separado para no bloquear el teclado
    threading.Thread(target=_run_gui, daemon=True).start()

def alternar_navegador():
    actual = leer_estado_actual()
    
    if actual == "brave":
        # Cambiar a Opera
        guardar_estado("opera")
        # Mostrar mensaje Rojo (Opera GX)
        mostrar_tooltip("⭕ Opera GX Activado", "#fa0f00") # Rojo neón
    else:
        # Cambiar a Brave
        guardar_estado("brave")
        # Mostrar mensaje Naranja (Brave)
        mostrar_tooltip("🦁 Brave Activado", "#ff5500") # Naranja

# --- Configuración del Atajo ---
# Usamos 'right alt+b' para AltGr + B
keyboard.add_hotkey('alt gr+b', alternar_navegador)

# Si tienes problemas, descomenta la siguiente línea para probar:
# keyboard.add_hotkey('ctrl+b', alternar_navegador)

print("Controlador visual iniciado. Presiona AltGr+B")

# Aseguramos estado inicial
if not os.path.exists(ARCHIVO_ESTADO):
    guardar_estado("brave")

keyboard.wait()