# theme_manager.py
import os
from PyQt6.QtGui import QAction
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def set_theme(window, theme_file):
    theme_folder = os.path.join(BASE_DIR, 'themes')
    theme_path = os.path.join(theme_folder, theme_file)
    with open(theme_path, 'r') as f:
        style_sheet = f.read()
    window.setStyleSheet(style_sheet)
def create_theme_actions(window, theme_menu):
    # Dictionary mapping theme names to their file names and shortcut keys
    themes_info = [
        ('Modern Apple Light', 'ModernAppleLightWithAccent.qss', 'Ctrl+1'),
        ('Apple Dark Light Hybrid', 'AppleDarkLightHybrid.qss', 'Ctrl+2'),
        ('Classic Apple Light', 'ClassicAppleLight.qss', 'Ctrl+3'),
        ('Elegant Dark', 'ElegantDarkTheme.qss', 'Ctrl+4'),
        ('Soft Blue', 'SoftBlueTheme.qss', 'Ctrl+5'),
        ('Minimalist Green', 'MinimalistGreenTheme.qss', 'Ctrl+6'),
        ('Warm Sunset', 'WarmSunsetTheme.qss', 'Ctrl+7'),
        ('Retro Wave', 'RetroWaveTheme.qss', 'Ctrl+8'),
        ('Nature Inspired', 'NatureInspiredTheme.qss', 'Ctrl+9'),
        ('Tech Professional', 'TechProfessionalTheme.qss', 'Ctrl+0'),
    ]
    # Create an action for each theme
    for theme_name, theme_file, shortcut_key in themes_info:
        theme_action = QAction(theme_name, window)
        theme_action.setShortcut(shortcut_key)
        theme_action.triggered.connect(lambda checked, file=theme_file: set_theme(window, file))
        theme_menu.addAction(theme_action)
def set_default_theme(window):
    set_theme(window, 'ModernAppleLightWithAccent.qss')
