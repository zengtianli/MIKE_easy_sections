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
    theme_actions = {
        'Modern Apple Light': lambda: set_theme(window, 'ModernAppleLightWithAccent.qss'),
        'Apple Dark Light Hybrid': lambda: set_theme(window, 'AppleDarkLightHybrid.qss'),
        'Classic Apple Light': lambda: set_theme(window, 'ClassicAppleLight.qss'),
        'Elegant Dark': lambda: set_theme(window, 'ElegantDarkTheme.qss'),
        'Soft Blue': lambda: set_theme(window, 'SoftBlueTheme.qss'),
        'Minimalist Green': lambda: set_theme(window, 'MinimalistGreenTheme.qss'),
        'Warm Sunset': lambda: set_theme(window, 'WarmSunsetTheme.qss'),
        'Retro Wave': lambda: set_theme(window, 'RetroWaveTheme.qss'),
        'Nature Inspired': lambda: set_theme(window, 'NatureInspiredTheme.qss'),
        'Tech Professional': lambda: set_theme(window, 'TechProfessionalTheme.qss'),
    }

    for theme_name, theme_func in theme_actions.items():
        theme_action = QAction(theme_name, window)
        theme_action.triggered.connect(theme_func)
        theme_menu.addAction(theme_action)

def set_default_theme(window):
    set_theme(window, 'ModernAppleLightWithAccent.qss')

