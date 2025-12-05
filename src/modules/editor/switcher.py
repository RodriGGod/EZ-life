"""
Editor switching module for EZLife Tool.
Handles code editor rotation and switching logic.
"""
from modules.base_module import BaseModule
from modules.editor.detector import detect_editors
from utils.tooltip import show_tooltip


class EditorModule(BaseModule):
    """Code editor switching module implementation."""
    
    def __init__(self, config):
        super().__init__(config)
        self.module_name = 'editor'
    
    def detect_targets(self):
        """Detect installed code editors."""
        return detect_editors()
    
    def get_active_targets(self):
        """Get user-selected active editors."""
        config_data = self.config.data
        return config_data.get('editores_activos', [])
    
    def set_active_targets(self, targets):
        """Set active editors."""
        config_data = self.config.data
        config_data['editores_activos'] = targets
        return self.config.save(config_data)
    
    def get_current_target(self):
        """Get currently selected editor."""
        active = self.get_active_targets()
        if not active:
            return None
        
        idx = self.config.get('indice_editor_actual', 0)
        if idx >= len(active):
            idx = 0
        
        return active[idx]
    
    def switch_to_next(self):
        """Switch to next editor in rotation."""
        active = self.get_active_targets()
        if not active:
            return None
        
        # Calculate next index
        idx = self.config.get('indice_editor_actual', 0)
        next_idx = (idx + 1) % len(active)
        
        # Save new index
        self.config.set('indice_editor_actual', next_idx)
        
        # Get new current editor
        new_editor = active[next_idx]
        
        # Show visual feedback
        show_tooltip(f"💻 Cambiado a: {new_editor['nombre']}")
        
        return new_editor
    
    def get_hotkey(self):
        """Get editor switching hotkey."""
        return self.config.get('atajo_editor', 'alt gr+e')
    
    def set_hotkey(self, hotkey):
        """Set editor switching hotkey."""
        return self.config.set('atajo_editor', hotkey)
