import tkinter as tk
from tkinter import messagebox, filedialog # Necesario para buscar archivos manuales
import json
import os
import sys
import psutil
import keyboard # Necesario para escuchar el atajo

# --- Rutas ---
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

# Lista base de búsqueda automática
NAVEGADORES_COMUNES = {
    "Brave": [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
    ],
    "Opera GX": [
        os.path.expanduser(r"~\AppData\Local\Programs\Opera GX\launcher.exe"),
        os.path.expanduser(r"~\AppData\Local\Programs\Opera\launcher.exe"), # A veces se instala aquí
        r"C:\Program Files\Opera GX\launcher.exe"
    ],
    "Chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ],
    "Firefox": [
        r"C:\Program Files\Mozilla Firefox\firefox.exe"
    ],
    "Edge": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]
}

class AppAccesibilidad:
    def __init__(self, root):
        self.root = root
        
        # --- [ZONA DE DISEÑO] Configuración General ---
        self.root.title("Switch Browser Config")
        self.root.geometry("450x550") # Tamaño de la ventana (Ancho x Alto)
        self.root.configure(bg="#f0f0f0") # Color de fondo general (Gris claro)
        
        # Estilos de fuentes (Puedes cambiarlas aquí)
        self.font_titulo = ("Segoe UI", 12, "bold")
        self.font_texto = ("Segoe UI", 10)
        
        # ------------------------------------------------
        # 1. SECCIÓN ATAJO DE TECLADO
        # ------------------------------------------------
        frame_atajo = tk.Frame(root, bg="white", padx=10, pady=10, relief="groove", bd=1)
        frame_atajo.pack(pady=15, padx=20, fill="x")

        tk.Label(frame_atajo, text="1. Configurar Atajo:", font=self.font_titulo, bg="white").pack(anchor="w")

        # Contenedor horizontal para entry y botón
        row_atajo = tk.Frame(frame_atajo, bg="white")
        row_atajo.pack(fill="x", pady=5)

        self.entry_atajo = tk.Entry(row_atajo, font=("Consolas", 12), justify="center", bg="#e8e8e8")
        self.entry_atajo.insert(0, "alt gr+b")
        self.entry_atajo.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botón para grabar
        self.btn_grabar = tk.Button(row_atajo, text="🎤 Grabar", bg="#2196F3", fg="white",
                                    font=("Segoe UI", 9, "bold"), command=self.escuchar_atajo)
        self.btn_grabar.pack(side="right")
        
        tk.Label(frame_atajo, text="Pulsa 'Grabar' y presiona tu combinación.", 
                 fg="gray", bg="white", font=("Arial", 8)).pack(anchor="w")

        # ------------------------------------------------
        # 2. SECCIÓN NAVEGADORES
        # ------------------------------------------------
        frame_nav = tk.Frame(root, bg="white", padx=10, pady=10, relief="groove", bd=1)
        frame_nav.pack(pady=5, padx=20, fill="both", expand=True)

        tk.Label(frame_nav, text="2. Seleccionar Navegadores:", font=self.font_titulo, bg="white").pack(anchor="w")

        # Frame con scroll para la lista
        self.canvas_lista = tk.Canvas(frame_nav, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(frame_nav, orient="vertical", command=self.canvas_lista.yview)
        self.scroll_frame = tk.Frame(self.canvas_lista, bg="white")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas_lista.configure(scrollregion=self.canvas_lista.bbox("all"))
        )

        self.canvas_lista.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas_lista.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_lista.pack(side="left", fill="both", expand=True, pady=5)
        self.scrollbar.pack(side="right", fill="y", pady=5)

        # Variables para guardar info
        self.lista_navegadores_ui = [] # Guardará referencias a los checkboxes

        # Cargar navegadores detectados automáticamente
        self.cargar_navegadores_auto()

        # Botón Añadir Manualmente
        btn_add = tk.Button(frame_nav, text="+ Añadir Manualmente (.exe)", 
                            command=self.anadir_manual,
                            bg="#ff9800", fg="white", font=("Segoe UI", 9))
        btn_add.pack(pady=5, fill="x")

        # ------------------------------------------------
        # 3. BOTÓN GUARDAR
        # ------------------------------------------------
        btn_guardar = tk.Button(root, text="GUARDAR Y APLICAR", 
                                bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"),
                                command=self.guardar_config, cursor="hand2")
        btn_guardar.pack(pady=20, ipadx=20, ipady=5)

    def escuchar_atajo(self):
        """Escucha la siguiente combinación de teclas"""
        self.btn_grabar.config(text="Escuchando...", bg="red")
        self.root.update()
        
        try:
            # Lee el atajo (bloquea la app momentáneamente hasta que pulsas)
            atajo = keyboard.read_hotkey(suppress=False)
            
            # Limpiar y poner el nuevo
            self.entry_atajo.delete(0, tk.END)
            self.entry_atajo.insert(0, atajo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo detectar: {e}")
        
        self.btn_grabar.config(text="🎤 Grabar", bg="#2196F3")

    def anadir_manual(self):
        """Abre explorador de archivos para buscar .exe"""
        ruta = filedialog.askopenfilename(
            title="Selecciona el ejecutable del navegador",
            filetypes=[("Ejecutables", "*.exe"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            nombre = os.path.basename(ruta).replace(".exe", "").capitalize()
            # Añadir a la lista visual
            self.agregar_checkbox(nombre, ruta, marcado=True)

    def agregar_checkbox(self, nombre, ruta, marcado=False):
        """Crea un checkbox en la lista visual"""
        var = tk.BooleanVar(value=marcado)
        chk = tk.Checkbutton(self.scroll_frame, text=f"{nombre}", variable=var, 
                             bg="white", font=self.font_texto, anchor="w")
        
        # Tooltip simple (nombre de ruta al pasar mouse) opcional
        # chk.bind("<Enter>", lambda e: self.root.title(f"Ruta: {ruta}"))

        chk.pack(fill="x", pady=2)
        
        self.lista_navegadores_ui.append({
            "nombre": nombre,
            "ruta": ruta,
            "var": var
        })

    def cargar_navegadores_auto(self):
        """Busca en el PC y rellena la lista"""
        for nombre, rutas in NAVEGADORES_COMUNES.items():
            for ruta in rutas:
                if os.path.exists(ruta):
                    self.agregar_checkbox(nombre, ruta, marcado=False)
                    break # Si encuentra una ruta válida para ese navegador, para de buscar

    def guardar_config(self):
        atajo = self.entry_atajo.get()
        seleccionados = []
        
        for item in self.lista_navegadores_ui:
            if item["var"].get():
                seleccionados.append({
                    "nombre": item["nombre"],
                    "ruta": item["ruta"]
                })

        if not seleccionados:
            messagebox.showwarning("Cuidado", "Debes seleccionar al menos un navegador.")
            return

        data = {
            "atajo": atajo,
            "navegadores_activos": seleccionados,
            "indice_actual": 0
        }

        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            
            self.reiniciar_controlador()
            messagebox.showinfo("Listo", "Configuración guardada.\nPuedes cerrar esta ventana.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def reiniciar_controlador(self):
        nombre_proceso = "controlador.exe"
        # Matar proceso
        for proc in psutil.process_iter():
            try:
                if proc.name() == nombre_proceso:
                    proc.kill()
            except: pass
        
        # Iniciar nuevo
        ruta_controlador = os.path.join(BASE_DIR, nombre_proceso)
        if os.path.exists(ruta_controlador):
            os.startfile(ruta_controlador)
        else:
            # Modo desarrollo (.py)
            ruta_py = os.path.join(BASE_DIR, "controlador.py")
            if os.path.exists(ruta_py):
               os.system(f'start python "{ruta_py}"')

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAccesibilidad(root)
    root.mainloop()