# plugins/sample_plugin.py
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface


class Plugin(PluginInterface):
    def initialize(self, window, plugins_menu):
        self.window = window
        self.add_menu_item(plugins_menu)

    def add_menu_item(self, plugins_menu):
        action = QAction("Say Hello", self.window)
        action.triggered.connect(self.say_hello)
        plugins_menu.addAction(action)

    def say_hello(self):
        print("Hello from the plugin!")
