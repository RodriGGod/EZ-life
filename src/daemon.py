"""
EZLife Tool - Background Daemon Entry Point
Listens for hotkeys and manages module switching.
"""
import keyboard
import time
from core.config import get_config
from modules.browser.switcher import BrowserModule


def main():
    """Start the background daemon."""
    print("Iniciando EZLife Daemon...")
    
    config = get_config()
    config.load()
    
    # Initialize browser module
    browser_module = BrowserModule(config)
    
    # Get hotkey from config
    hotkey = browser_module.get_hotkey()
    
    if not hotkey:
        print("No hay configuración válida. Ejecuta la App primero.")
        time.sleep(5)
        return
    
    print(f"Escuchando atajo: {hotkey}")
    
    try:
        # Register hotkey for browser switching
        keyboard.add_hotkey(hotkey, browser_module.switch_to_next)
        
        # TODO: Add more modules here as they are implemented
        # editor_module = EditorModule(config)
        # keyboard.add_hotkey(editor_module.get_hotkey(), editor_module.switch_to_next)
        
        # Keep daemon running
        keyboard.wait()
    except Exception as e:
        print(f"Error en el daemon: {e}")
        time.sleep(5)


if __name__ == "__main__":
    main()
