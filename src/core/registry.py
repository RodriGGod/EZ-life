"""
Windows Registry operations for EZLife Tool.
Handles autostart configuration and application detection.
"""
import winreg
import os
from core.paths import get_executable_path


class RegistryManager:
    """Manages Windows Registry operations."""
    
    STARTUP_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "EZLifeController"
    
    @staticmethod
    def enable_autostart():
        """
        Enable autostart by adding entry to Windows Registry.
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            controlador_path = get_executable_path("controlador")
            
            # Wrap .py files in python command
            if controlador_path.endswith('.py'):
                controlador_path = f'python "{controlador_path}"'
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RegistryManager.STARTUP_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            
            winreg.SetValueEx(
                key,
                RegistryManager.APP_NAME,
                0,
                winreg.REG_SZ,
                controlador_path
            )
            winreg.CloseKey(key)
            
            return {"success": True, "message": "✅ Inicio automático activado"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    @staticmethod
    def disable_autostart():
        """
        Disable autostart by removing entry from Windows Registry.
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RegistryManager.STARTUP_KEY_PATH,
                0,
                winreg.KEY_SET_VALUE
            )
            
            try:
                winreg.DeleteValue(key, RegistryManager.APP_NAME)
                winreg.CloseKey(key)
                return {"success": True, "message": "❌ Inicio automático desactivado"}
            except FileNotFoundError:
                winreg.CloseKey(key)
                return {"success": True, "message": "Ya estaba desactivado"}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
    
    @staticmethod
    def check_autostart_status():
        """
        Check if autostart is currently enabled.
        
        Returns:
            dict: {"enabled": bool, "path": str (optional), "error": str (optional)}
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                RegistryManager.STARTUP_KEY_PATH,
                0,
                winreg.KEY_READ
            )
            
            try:
                value, _ = winreg.QueryValueEx(key, RegistryManager.APP_NAME)
                winreg.CloseKey(key)
                return {"enabled": True, "path": value}
            except FileNotFoundError:
                winreg.CloseKey(key)
                return {"enabled": False}
        except Exception as e:
            return {"enabled": False, "error": str(e)}
    
    @staticmethod
    def toggle_autostart(enable):
        """
        Toggle autostart on or off.
        
        Args:
            enable: True to enable, False to disable
        
        Returns:
            dict: {"success": bool, "message": str}
        """
        if enable:
            return RegistryManager.enable_autostart()
        else:
            return RegistryManager.disable_autostart()
