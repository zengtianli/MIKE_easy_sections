# plugins/theme_plugin.py
from PyQt6.QtGui import QAction
from plugin_interface import PluginInterface
import os,json
from constants import PLUGIN_CONFIG_FILE
class Plugin(PluginInterface):
    def initialize(self, window, menu):
        self.window = window
        self.create_theme_menu(menu)
    def create_theme_menu(self, menu):
        theme_menu = menu.addMenu('Themes')
        self.create_theme_actions(theme_menu)
    def create_theme_actions(self, theme_menu):
        themes_info = [
            ('Apple Dark Light Hybrid', 'AppleDarkLightHybrid.qss', 'Ctrl+1'),
            ('Classic Apple Light', 'ClassicAppleLight.qss', 'Ctrl+2'),
            ('Elegant Dark', 'ElegantDarkTheme.qss', 'Ctrl+3'),
            ('Minimalist Green', 'MinimalistGreenTheme.qss', 'Ctrl+4'),
            ('Modern Apple Light', 'ModernAppleLightWithAccent.qss', 'Ctrl+5'),
            ('Nature Inspired', 'NatureInspiredTheme.qss', 'Ctrl+6'),
            ('Retro Wave', 'RetroWaveTheme.qss', 'Ctrl+7'),
            ('Soft Blue', 'SoftBlueTheme.qss', 'Ctrl+8'),
            ('Tech Professional', 'TechProfessionalTheme.qss', 'Ctrl+9'),
            ('Warm Sunset', 'WarmSunsetTheme.qss', 'Ctrl+0'),
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
        self.save_theme_config(theme_file)
    def save_theme_config(self, theme_file):
        config_key = 'theme_plugin'  # Plugin name without .py
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config[config_key] = {'saved_setting': theme_file}
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)
    def load_settings(self, settings):
        if 'saved_setting' in settings:
            self.set_theme(settings['saved_setting'])
    def deinitialize(self, window, menu):
        # Find and remove the 'Themes' menu from the menu bar
        for action in menu.actions():
            if action.text() == 'Themes':
                menu.removeAction(action)
                break
