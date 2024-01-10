# plugins/theme_manager_plugin.py
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface
import os


class Plugin(PluginInterface):
    def initialize(self, window, menu):
        self.window = window
        self.create_theme_menu(menu)

    def create_theme_menu(self, menu):
        theme_menu = menu.addMenu('Themes')
        self.create_theme_actions(theme_menu)
        self.set_default_theme(theme_menu)

    def create_theme_actions(self, theme_menu):
        # Define themes and their corresponding files
        themes_info = [
            ('Modern Apple Light', 'ModernAppleLightWithAccent.qss', 'Ctrl+1'),
            # ... other themes ...
        ]
        for theme_name, theme_file, shortcut_key in themes_info:
            theme_action = QAction(theme_name, self.window)
            theme_action.setShortcut(shortcut_key)
            theme_action.triggered.connect(
                lambda checked, file=theme_file: self.set_theme(file))
            theme_menu.addAction(theme_action)

    def set_theme(self, theme_file):
        theme_folder = os.path.join(os.path.dirname(__file__), 'themes')
        theme_path = os.path.join(theme_folder, theme_file)
        with open(theme_path, 'r') as f:
            style_sheet = f.read()
        self.window.setStyleSheet(style_sheet)

    def set_default_theme(self, theme_menu):
        default_theme = 'ModernAppleLightWithAccent.qss'
        self.set_theme(default_theme)
