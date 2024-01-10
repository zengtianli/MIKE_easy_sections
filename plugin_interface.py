# plugin_interface.py

class PluginInterface:
    def initialize(self, window, menu):
        """Initialize the plugin with the main application window and plugins menu."""
        raise NotImplementedError

