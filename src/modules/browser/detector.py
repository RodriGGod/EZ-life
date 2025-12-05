"""
Browser detection module for EZLife Tool.
Detects installed web browsers from Windows Registry and common installation paths.
"""
import winreg
import os


def detect_browsers():
    """
    Detect installed web browsers on the system.
    
    Returns:
        list: List of dictionaries with 'nombre' and 'ruta' keys
    """
    encontrados = []
    rutas_vistas = set()
    
    # 1. Search Windows Registry
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
                            # Normalize common browser names
                            if "Opera GX" in name or "OperaGX" in exe_path:
                                display_name = "Opera GX"
                            if "Brave" in name:
                                display_name = "Brave Browser"
                            
                            encontrados.append({"nombre": display_name, "ruta": exe_path})
                            rutas_vistas.add(exe_path)
                    except:
                        continue
            except:
                continue
    
    # 2. Search manually in common AppData locations
    user_home = os.path.expanduser("~")
    rutas_extra = [
        (os.path.join(user_home, r"AppData\Local\Programs\Opera GX\launcher.exe"), "Opera GX"),
        (os.path.join(user_home, r"AppData\Local\Programs\Opera\launcher.exe"), "Opera"),
        (r"C:\Program Files\Opera GX\launcher.exe", "Opera GX"),
        (os.path.join(user_home, r"AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"), "Brave Browser"),
        (r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", "Brave Browser"),
    ]
    
    for path, name in rutas_extra:
        if os.path.exists(path) and path not in rutas_vistas:
            encontrados.append({"nombre": name, "ruta": path})
            rutas_vistas.add(path)
    
    return encontrados


def is_browser_installed(browser_name):
    """
    Check if a specific browser is installed.
    
    Args:
        browser_name: Name of the browser to check
    
    Returns:
        bool: True if browser is found
    """
    browsers = detect_browsers()
    return any(browser_name.lower() in b['nombre'].lower() for b in browsers)


def get_browser_path(browser_name):
    """
    Get the executable path for a specific browser.
    
    Args:
        browser_name: Name of the browser
    
    Returns:
        str or None: Path to browser executable, or None if not found
    """
    browsers = detect_browsers()
    for browser in browsers:
        if browser_name.lower() in browser['nombre'].lower():
            return browser['ruta']
    return None
