"""
PyWebview API for EZLife Tool configuration interface.
Bridges JavaScript frontend with Python backend.
"""
import keyboard
import tkinter as tk
from tkinter import filedialog
import os

from core.config import get_config
from core.registry import RegistryManager
from core.paths import get_executable_path
from modules.browser.detector import detect_browsers
from utils.process import restart_process


class ConfigAPI:
    """API class for PyWebview configuration interface."""
    
    def __init__(self):
        self.config = get_config()
    
    def get_data_inicial(self):
        """
        Get initial data for the UI.
        
        Returns:
            dict: Configuration data, detected browsers, browser path, and autostart status
        """
        self.config.load()
        
        # Get browser proxy path
        browser_path = get_executable_path("proxy")
        if not os.path.exists(browser_path):
            browser_path = "EZLife_Browser.exe not found (Build it first!)"
        
        # Check autostart status
        autostart_status = RegistryManager.check_autostart_status()
        
        return {
            "config": self.config.data,
            "sistema": detect_browsers(),
            "browserPath": browser_path,
            "autostartEnabled": autostart_status.get("enabled", False)
        }
    
    def grabar_atajo(self):
        """
        Record a keyboard shortcut.
        Blocks until user presses keys.
        
        Returns:
            str: Recorded hotkey string
        """
        return keyboard.read_hotkey(suppress=False)
    
    def examinar_exe(self):
        """
        Open file dialog to select an executable.
        
        Returns:
            dict or None: {"nombre": str, "ruta": str} or None if cancelled
        """
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
        """
        Save configuration and restart the daemon.
        
        Args:
            atajo: Hotkey string
            lista_activos: List of active browsers
        
        Returns:
            bool: True if successful
        """
        data = {
            "atajo": atajo,
            "navegadores_activos": lista_activos,
            "indice_actual": 0
        }
        
        try:
            if self.config.save(data):
                restart_process("daemon")
                return True
            return False
        except Exception as e:
            print(f"Error saving config: {e}")
            return str(e)
    
    def cerrar_app(self):
        """Close the application."""
        os._exit(0)
    
    def open_default_apps(self):
        """Open Windows default apps settings."""
        os.system('start ms-settings:defaultapps')
    
    def toggle_autostart(self, enable):
        """
        Toggle autostart on or off.
        
        Args:
            enable: True to enable, False to disable
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        return RegistryManager.toggle_autostart(enable)
    
    def check_autostart_status(self):
        """
        Check autostart status.
        
        Returns:
            dict: {"enabled": bool, "path": str (optional)}
        """
        return RegistryManager.check_autostart_status()
