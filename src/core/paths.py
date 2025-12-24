"""
Path resolution utilities for EZLife Tool.
Handles all path-related operations including AppData, executable paths, and resource directories.
"""
import os
import sys


def get_base_dir():
    """
    Get the base directory for the application.
    Returns sys._MEIPASS when frozen (PyInstaller), otherwise the script directory.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running as Python script
        return os.path.dirname(os.path.abspath(__file__ + "/../"))


def get_app_data_dir():
    """
    Get the AppData directory for storing user configuration.
    Creates the directory if it doesn't exist.
    """
    app_data_dir = os.path.join(os.getenv('APPDATA'), 'EZLifeTool')
    if not os.path.exists(app_data_dir):
        try:
            os.makedirs(app_data_dir)
        except Exception:
            pass
    return app_data_dir


def get_config_file():
    """Get the full path to the configuration file."""
    return os.path.join(get_app_data_dir(), 'config.json')


def get_web_dir():
    """Get the path to the web UI directory."""
    return os.path.join(get_base_dir(), 'ui', 'web')


def get_install_dir():
    """
    Get the installation directory (where executables are located).
    Returns the directory containing the executable when frozen, otherwise the dist directory.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        # In development, executables are in dist/
        return os.path.join(get_base_dir(), 'dist')


def get_executable_path(name):
    """
    Get the full path to an executable.
    
    Args:
        name: Name of the executable (e.g., 'controlador', 'browser', 'proxy')
    
    Returns:
        Full path to the executable (.exe when frozen, .py in development)
    """
    # Map internal names to actual executable names
    name_mapping = {
        'proxy': 'EZLife_Browser',
        'browser': 'EZLife_Browser',
        'daemon': 'controlador',
    }
    
    # Use mapped name if available
    exe_name = name_mapping.get(name, name)
    
    install_dir = get_install_dir()
    
    if getattr(sys, 'frozen', False):
        # Look for .exe
        exe_path = os.path.join(install_dir, f"{exe_name}.exe")
        if os.path.exists(exe_path):
            return exe_path
    
    # Look for .py script (use original name for scripts)
    base_dir = get_base_dir()
    py_path = os.path.join(base_dir, f"{name}.py")
    if os.path.exists(py_path):
        return py_path
    
    # Return expected .exe path even if it doesn't exist
    return os.path.join(install_dir, f"{exe_name}.exe")
