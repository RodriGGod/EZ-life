"""
Browser proxy module for EZLife Tool.
Handles opening URLs in the currently selected browser.
"""
import subprocess
import os
from core.config import get_config


def open_url(url):
    """
    Open a URL in the currently selected browser.
    
    Args:
        url: URL to open
    """
    config = get_config()
    config.load()
    
    # Fallback if no configuration
    if not config.get('navegadores_activos'):
        os.system(f'start chrome "{url}"')
        return
    
    # Get current browser
    idx = config.get('indice_actual', 0)
    browsers = config.get('navegadores_activos', [])
    
    # Ensure index is valid
    if idx >= len(browsers):
        idx = 0
    
    browser_data = browsers[idx]
    ruta_exe = browser_data['ruta']
    
    try:
        subprocess.Popen([ruta_exe, url])
    except Exception as e:
        # Fallback: try to open by name
        try:
            os.system(f'start {browser_data["nombre"]} "{url}"')
        except:
            # Last resort: use default browser
            os.system(f'start "" "{url}"')
