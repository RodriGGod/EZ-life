"""
Configuration management for EZLife Tool.
Handles reading, writing, and validating configuration files.
"""
import json
import os
from core.paths import get_config_file


class Config:
    """Configuration manager for EZLife Tool."""
    
    def __init__(self):
        self.config_file = get_config_file()
        self._data = None
    
    def load(self):
        """
        Load configuration from file.
        
        Returns:
            dict: Configuration data, or empty dict if file doesn't exist or is invalid
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
                    return self._data
            except Exception as e:
                print(f"Error loading config: {e}")
        
        self._data = {}
        return self._data
    
    def save(self, data):
        """
        Save configuration to file.
        
        Args:
            data: Configuration dictionary to save
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self._data = data
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
        
        Returns:
            Configuration value or default
        """
        if self._data is None:
            self.load()
        return self._data.get(key, default)
    
    def set(self, key, value):
        """
        Set a configuration value and save.
        
        Args:
            key: Configuration key
            value: Value to set
        
        Returns:
            bool: True if successful
        """
        if self._data is None:
            self.load()
        self._data[key] = value
        return self.save(self._data)
    
    def update(self, updates):
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of key-value pairs to update
        
        Returns:
            bool: True if successful
        """
        if self._data is None:
            self.load()
        self._data.update(updates)
        return self.save(self._data)
    
    @property
    def data(self):
        """Get the full configuration data."""
        if self._data is None:
            self.load()
        return self._data


# Singleton instance
_config_instance = None


def get_config():
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
