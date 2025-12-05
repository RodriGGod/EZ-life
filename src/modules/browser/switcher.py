"""
Browser switching module for EZLife Tool.
Handles browser rotation and switching logic.
"""
from modules.base_module import BaseModule
from modules.browser.detector import detect_browsers
from utils.tooltip import show_tooltip


class BrowserModule(BaseModule):
    """Browser switching module implementation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.module_name = 'browser'
    
    def detect_targets(self):
        """Detect installed browsers."""
        return detect_browsers()
    
    def get_active_targets(self):
        """Get user-selected active browsers."""
        config_data = self.config.data
        return config_data.get('navegadores_activos', [])
    
    def set_active_targets(self, targets):
        """Set active browsers."""
        config_data = self.config.data
        config_data['navegadores_activos'] = targets
        return self.config.save(config_data)
    
    def get_current_target(self):
        """Get currently selected browser."""
        active = self.get_active_targets()
        if not active:
            return None
        
        idx = self.config.get('indice_actual', 0)
        if idx >= len(active):
            idx = 0
        
        return active[idx]
    
    def switch_to_next(self):
        """Switch to next browser in rotation."""
        active = self.get_active_targets()
        if not active:
            return None
        
        # Calculate next index
        idx = self.config.get('indice_actual', 0)
        next_idx = (idx + 1) % len(active)
        
        # Save new index
        self.config.set('indice_actual', next_idx)
        
        # Get new current browser
        new_browser = active[next_idx]
        
        # Show visual feedback
        show_tooltip(f"🌍 Cambiado a: {new_browser['nombre']}")
        
        return new_browser
    
    def get_hotkey(self):
        """Get browser switching hotkey."""
        return self.config.get('atajo', 'alt gr+b')
    
    def set_hotkey(self, hotkey):
        """Set browser switching hotkey."""
        return self.config.set('atajo', hotkey)
    
    def get_current_index(self):
        """Get current browser index."""
        return self.config.get('indice_actual', 0)
    
    def set_current_index(self, index):
        """Set current browser index."""
        return self.config.set('indice_actual', index)
