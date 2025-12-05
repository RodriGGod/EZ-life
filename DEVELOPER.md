# EZLife Tool - Developer Documentation

## Project Structure

```
src/
├── main.py                    # Entry point: Configuration GUI
├── daemon.py                  # Entry point: Background hotkey daemon
├── proxy.py                   # Entry point: Browser proxy
│
├── core/                      # Core shared functionality
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── paths.py               # Path resolution utilities
│   └── registry.py            # Windows Registry operations
│
├── modules/                   # Feature modules (pluggable architecture)
│   ├── __init__.py
│   ├── base_module.py         # Base class for all modules
│   ├── browser/               # Browser switching module
│   │   ├── __init__.py
│   │   ├── detector.py        # Browser detection
│   │   ├── switcher.py        # Browser switching logic
│   │   └── proxy.py           # URL handler
│   └── editor/                # Code editor module
│       ├── __init__.py
│       ├── detector.py        # Editor detection
│       └── switcher.py        # Editor switching logic
│
├── ui/                        # User interface
│   ├── __init__.py
│   ├── api.py                 # PyWebview API bridge
│   └── web/                   # HTML/CSS/JS files
│       ├── index.html
│       └── style.css
│
├── utils/                     # Utilities
│   ├── __init__.py
│   ├── process.py             # Process management
│   └── tooltip.py             # Visual feedback
│
├── build/                     # Build artifacts (old spec files)
├── dist/                      # Compiled executables
│
├── main.spec                  # PyInstaller spec for config GUI
├── daemon.spec                # PyInstaller spec for daemon
└── proxy.spec                 # PyInstaller spec for proxy
```

## Module System

### Creating a New Module

All feature modules should inherit from `BaseModule` and implement the required methods:

```python
from modules.base_module import BaseModule

class MyModule(BaseModule):
    def __init__(self, config):
        super().__init__(config)
        self.module_name = 'mymodule'
    
    def detect_targets(self):
        # Detect available targets
        return [{"nombre": "Target 1", "ruta": "/path/to/target1"}]
    
    def get_active_targets(self):
        # Get user-selected targets from config
        return self.config.get('mymodule_activos', [])
    
    def set_active_targets(self, targets):
        # Save active targets to config
        return self.config.set('mymodule_activos', targets)
    
    def get_current_target(self):
        # Get currently selected target
        active = self.get_active_targets()
        idx = self.config.get('mymodule_index', 0)
        return active[idx] if active else None
    
    def switch_to_next(self):
        # Switch to next target
        active = self.get_active_targets()
        idx = self.config.get('mymodule_index', 0)
        next_idx = (idx + 1) % len(active)
        self.config.set('mymodule_index', next_idx)
        return active[next_idx]
    
    def get_hotkey(self):
        # Get module hotkey
        return self.config.get('mymodule_hotkey', 'alt gr+m')
    
    def set_hotkey(self, hotkey):
        # Set module hotkey
        return self.config.set('mymodule_hotkey', hotkey)
```

### Registering a Module in the Daemon

Edit `daemon.py` to register your module:

```python
from modules.mymodule.switcher import MyModule

# In main():
my_module = MyModule(config)
keyboard.add_hotkey(my_module.get_hotkey(), my_module.switch_to_next)
```

## Building

### Development Mode

Run directly with Python:

```bash
python src/main.py        # Configuration GUI
python src/daemon.py      # Background daemon
python src/proxy.py       # Browser proxy
```

### Production Build

Compile with PyInstaller:

```bash
cd src
pyinstaller main.spec      # Creates dist/EZLife_Config.exe
pyinstaller daemon.spec    # Creates dist/daemon.exe
pyinstaller proxy.spec     # Creates dist/proxy.exe
```

## Configuration

Configuration is stored in `%APPDATA%\EZLifeTool\config.json`:

```json
{
    "atajo": "alt gr+b",
    "navegadores_activos": [
        {"nombre": "Brave Browser", "ruta": "C:\\...\\brave.exe"},
        {"nombre": "Chrome", "ruta": "C:\\...\\chrome.exe"}
    ],
    "indice_actual": 0,
    "atajo_editor": "alt gr+e",
    "editores_activos": [],
    "indice_editor_actual": 0
}
```

## Core Modules

### `core.config`

Manages configuration file reading/writing:

```python
from core.config import get_config

config = get_config()
config.load()
value = config.get('key', default_value)
config.set('key', value)
```

### `core.paths`

Resolves application paths:

```python
from core.paths import get_app_data_dir, get_executable_path

app_data = get_app_data_dir()  # %APPDATA%\EZLifeTool
exe_path = get_executable_path('daemon')  # Path to daemon.exe
```

### `core.registry`

Manages Windows Registry:

```python
from core.registry import RegistryManager

RegistryManager.enable_autostart()
status = RegistryManager.check_autostart_status()
```

## Utilities

### Process Management

```python
from utils.process import restart_process, kill_process_by_name

restart_process('daemon')  # Restart daemon.exe
kill_process_by_name('daemon.exe')
```

### Visual Feedback

```python
from utils.tooltip import show_tooltip, show_success, show_error

show_tooltip("Custom message")
show_success("Operation completed!")
show_error("Something went wrong")
```

## Migration from Old Structure

Old files have been renamed with `.old` extension:
- `app.py` → `app.py.old`
- `controlador.py` → `controlador.py.old`
- `browser.py` → `browser.py.old`

These can be deleted once the new structure is verified working.
