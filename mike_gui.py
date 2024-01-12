# mike_gui.py
from PyQt6.QtWidgets import QDialog
import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QTextEdit,QMenuBar, QMainWindow, QDialog)
from plugin_selection_dialog import PluginSelectionDialog
import importlib.util
import json
from constants import PLUGIN_CONFIG_FILE
from layout_manager import setup_layout_menus
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
plugins_folder = os.path.join(BASE_DIR, 'plugins')
loaded_plugins = {}

class PluginManager:
    def __init__(self, main_window: QMainWindow, menu_bar: QMenuBar):
        self.loaded_plugins = {}
        self.window = main_window
        self.menu_bar = menu_bar
    def load_plugin(self, plugin_file):
        plugin_path = os.path.join(plugins_folder, plugin_file)
        if os.path.isfile(plugin_path) and plugin_file.endswith('.py'):
            spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            if hasattr(plugin_module, 'Plugin'):
                plugin = plugin_module.Plugin()
                plugin.initialize(self.window, self.menu_bar)
                self.loaded_plugins[plugin_file] = plugin
        self.save_plugin_config()
    def remove_plugin(self, plugin_file):
        if plugin_file in self.loaded_plugins:
            plugin = self.loaded_plugins[plugin_file]
            if hasattr(plugin, 'deinitialize'):
                plugin.deinitialize(self.window, self.menu_bar)
            del self.loaded_plugins[plugin_file]
        self.save_plugin_config()
    def save_plugin_config(self):
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config['plugins'] = list(self.loaded_plugins.keys())
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)
    def load_plugin_config(self):
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
                plugin_files = config.get('plugins', [])
                for plugin_file in plugin_files:
                    self.load_plugin(plugin_file)
                # After all plugins are loaded, call a method to load their settings
                for plugin_file in plugin_files:
                    plugin_name = os.path.splitext(plugin_file)[0]
                    plugin_settings = config.get(plugin_name, {})
                    if plugin_file in self.loaded_plugins:
                        self.loaded_plugins[plugin_file].load_settings(plugin_settings)
    def open_plugin_selection(self):
        dialog = PluginSelectionDialog(plugins_folder, self.window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_plugin_file = dialog.selected_plugin()
            if selected_plugin_file:
                self.load_plugin(selected_plugin_file)
    def open_plugin_removal(self):
        dialog = PluginSelectionDialog(list(self.loaded_plugins.keys()), self.window)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_plugin_file = dialog.selected_plugin()
            if selected_plugin_file:
                self.remove_plugin(selected_plugin_file)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize the window
        self.setWindowTitle('MIKE Easy Section Converter')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.menu_bar = self.menuBar()
        self.plugins_menu = self.menu_bar.addMenu('Plugins')
        self.layout_menu = self.menu_bar.addMenu('Layout')
    def setup_menus(self, open_plugin_selection, open_plugin_removal, setup_layout_menus):
        plugin_selection_action = self.plugins_menu.addAction('Load Plugin')
        plugin_selection_action.triggered.connect(open_plugin_selection)
        plugin_removal_action = self.plugins_menu.addAction('Remove Plugin')
        plugin_removal_action.triggered.connect(open_plugin_removal)
        # setup_layout_menus(self.layout_menu, self, self.central_widget, self.output_area)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    plugin_manager = PluginManager(main_window, main_window.menu_bar)
    main_window.setup_menus(plugin_manager.open_plugin_selection, plugin_manager.open_plugin_removal, setup_layout_menus)
    plugin_manager.load_plugin_config()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
