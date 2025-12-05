"""
Base module class for EZLife feature modules.
Defines the interface that all feature modules must implement.
"""
from abc import ABC, abstractmethod


class BaseModule(ABC):
    """
    Base class for all EZLife feature modules.
    
    Each module (browser, editor, etc.) should inherit from this class
    and implement the required methods.
    """
    
    def __init__(self, config):
        """
        Initialize the module.
        
        Args:
            config: Configuration instance from core.config
        """
        self.config = config
        self.module_name = self.__class__.__name__.lower().replace('module', '')
    
    @abstractmethod
    def detect_targets(self):
        """
        Detect available targets for this module.
        
        For browser module: detect installed browsers
        For editor module: detect installed code editors
        
        Returns:
            list: List of dictionaries with 'name' and 'path' keys
        """
        pass
    
    @abstractmethod
    def get_active_targets(self):
        """
        Get the list of user-selected active targets.
        
        Returns:
            list: List of active target dictionaries
        """
        pass
    
    @abstractmethod
    def set_active_targets(self, targets):
        """
        Set the list of active targets.
        
        Args:
            targets: List of target dictionaries to set as active
        
        Returns:
            bool: True if successful
        """
        pass
    
    @abstractmethod
    def get_current_target(self):
        """
        Get the currently selected target.
        
        Returns:
            dict: Current target dictionary with 'name' and 'path'
        """
        pass
    
    @abstractmethod
    def switch_to_next(self):
        """
        Switch to the next target in the rotation.
        
        Returns:
            dict: The new current target
        """
        pass
    
    @abstractmethod
    def get_hotkey(self):
        """
        Get the hotkey for this module.
        
        Returns:
            str: Hotkey string (e.g., 'alt gr+b')
        """
        pass
    
    @abstractmethod
    def set_hotkey(self, hotkey):
        """
        Set the hotkey for this module.
        
        Args:
            hotkey: Hotkey string to set
        
        Returns:
            bool: True if successful
        """
        pass
    
    def get_config_key(self, key):
        """
        Get a module-specific configuration key.
        
        Args:
            key: Configuration key name
        
        Returns:
            Configuration value or None
        """
        module_config = self.config.get(self.module_name, {})
        return module_config.get(key)
    
    def set_config_key(self, key, value):
        """
        Set a module-specific configuration key.
        
        Args:
            key: Configuration key name
            value: Value to set
        
        Returns:
            bool: True if successful
        """
        module_config = self.config.get(self.module_name, {})
        module_config[key] = value
        return self.config.set(self.module_name, module_config)
