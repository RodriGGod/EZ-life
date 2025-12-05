"""
Code editor detection module for EZLife Tool.
Detects installed code editors from Windows Registry and common installation paths.
"""
import winreg
import os


def detect_editors():
    """
    Detect installed code editors on the system.
    
    Returns:
        list: List of dictionaries with 'nombre' and 'ruta' keys
    """
    encontrados = []
    rutas_vistas = set()
    
    user_home = os.path.expanduser("~")
    
    # Common editor paths
    editor_paths = [
        # VS Code
        (os.path.join(user_home, r"AppData\Local\Programs\Microsoft VS Code\Code.exe"), "Visual Studio Code"),
        (r"C:\Program Files\Microsoft VS Code\Code.exe", "Visual Studio Code"),
        
        # VS Code Insiders
        (os.path.join(user_home, r"AppData\Local\Programs\Microsoft VS Code Insiders\Code - Insiders.exe"), "VS Code Insiders"),
        
        # Sublime Text
        (r"C:\Program Files\Sublime Text\sublime_text.exe", "Sublime Text"),
        (r"C:\Program Files\Sublime Text 3\sublime_text.exe", "Sublime Text 3"),
        (r"C:\Program Files\Sublime Text 4\sublime_text.exe", "Sublime Text 4"),
        
        # Notepad++
        (r"C:\Program Files\Notepad++\notepad++.exe", "Notepad++"),
        (r"C:\Program Files (x86)\Notepad++\notepad++.exe", "Notepad++"),
        
        # Atom
        (os.path.join(user_home, r"AppData\Local\atom\atom.exe"), "Atom"),
        
        # JetBrains IDEs
        (r"C:\Program Files\JetBrains\IntelliJ IDEA\bin\idea64.exe", "IntelliJ IDEA"),
        (r"C:\Program Files\JetBrains\PyCharm\bin\pycharm64.exe", "PyCharm"),
        (r"C:\Program Files\JetBrains\WebStorm\bin\webstorm64.exe", "WebStorm"),
        
        # Vim
        (r"C:\Program Files\Vim\vim90\gvim.exe", "Vim"),
        (r"C:\Program Files (x86)\Vim\vim90\gvim.exe", "Vim"),
    ]
    
    for path, name in editor_paths:
        if os.path.exists(path) and path not in rutas_vistas:
            encontrados.append({"nombre": name, "ruta": path})
            rutas_vistas.add(path)
    
    return encontrados


def is_editor_installed(editor_name):
    """
    Check if a specific editor is installed.
    
    Args:
        editor_name: Name of the editor to check
    
    Returns:
        bool: True if editor is found
    """
    editors = detect_editors()
    return any(editor_name.lower() in e['nombre'].lower() for e in editors)


def get_editor_path(editor_name):
    """
    Get the executable path for a specific editor.
    
    Args:
        editor_name: Name of the editor
    
    Returns:
        str or None: Path to editor executable, or None if not found
    """
    editors = detect_editors()
    for editor in editors:
        if editor_name.lower() in editor['nombre'].lower():
            return editor['ruta']
    return None
