# mike_gui.py
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeySequence
import sys
import os
from PyQt6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox,
                             QTextEdit, QHBoxLayout, QMenuBar, QMainWindow, QDialog, QLabel, QLineEdit, QKeySequenceEdit)
from script_executor import (R_xlsx2csv, R_rename_csv, R_mks2chain, R_split_chg,
                             R_insert_chg, R_clean_csv, R_mkcc, R_get_virt_end, R_virt_start, R_virt_end,
                             R_upd_virt_end, R_combine_txt, R_conv_module, R_proc_module, R_virt_sect_mod)
from plugin_selection_dialog import PluginSelectionDialog
from plugins import layout_plugin
import importlib.util
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
plugins_folder = os.path.join(BASE_DIR, 'plugins')
loaded_plugins = {}
import json
# PLUGIN_CONFIG_FILE = os.path.join(BASE_DIR, 'plugin_config.json')
from constants import PLUGIN_CONFIG_FILE
# def save_plugin_config():
#     with open(PLUGIN_CONFIG_FILE, 'w') as file:
#         json.dump(list(loaded_plugins.keys()), file)

def save_plugin_config():
    config = {}
    if os.path.exists(PLUGIN_CONFIG_FILE):
        with open(PLUGIN_CONFIG_FILE, 'r') as file:
            config = json.load(file)
    config['plugins'] = list(loaded_plugins.keys())
    with open(PLUGIN_CONFIG_FILE, 'w') as file:
        json.dump(config, file)


def load_plugin_config():
    if os.path.exists(PLUGIN_CONFIG_FILE):
        with open(PLUGIN_CONFIG_FILE, 'r') as file:
            config = json.load(file)
            plugin_files = config.get('plugins', [])
            for plugin_file in plugin_files:
                load_plugin(plugin_file)

            # After all plugins are loaded, call a method to load their settings
            for plugin_file in plugin_files:
                plugin_name = os.path.splitext(plugin_file)[0]  # Remove .py extension
                plugin_settings = config.get(plugin_name, {})
                if plugin_file in loaded_plugins:
                    loaded_plugins[plugin_file].load_settings(plugin_settings)

def load_plugin(plugin_file):
    global loaded_plugins
    plugin_path = os.path.join(plugins_folder, plugin_file)
    if os.path.isfile(plugin_path) and plugin_file.endswith('.py'):
        spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        if hasattr(plugin_module, 'Plugin'):
            plugin = plugin_module.Plugin()
            plugin.initialize(window, menu_bar)
            loaded_plugins[plugin_file] = plugin
    save_plugin_config()

def remove_plugin(plugin_file):
    global loaded_plugins
    if plugin_file in loaded_plugins:
        plugin = loaded_plugins[plugin_file]
        if hasattr(plugin, 'deinitialize'):
            plugin.deinitialize(window, menu_bar)
        del loaded_plugins[plugin_file]
    save_plugin_config()
def open_plugin_selection():
    dialog = PluginSelectionDialog(plugins_folder, window)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        selected_plugin_file = dialog.selected_plugin()
        if selected_plugin_file:
            load_plugin(selected_plugin_file)
def open_plugin_removal():
    dialog = PluginSelectionDialog(list(loaded_plugins.keys()), window)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        selected_plugin_file = dialog.selected_plugin()
        if selected_plugin_file:
            remove_plugin(selected_plugin_file)
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('MIKE Easy Section Converter')
central_widget = QWidget()  
window.setCentralWidget(central_widget)
output_area = QTextEdit()
output_area.setReadOnly(True)
menu_bar = window.menuBar()
plugins_menu = menu_bar.addMenu('Plugins')
plugin_selection_action = plugins_menu.addAction('Load Plugin')
plugin_selection_action.triggered.connect(open_plugin_selection)
plugin_removal_action = plugins_menu.addAction('Remove Plugin')
plugin_removal_action.triggered.connect(open_plugin_removal)
layout_menu = menu_bar.addMenu('Layout')
layout_plugin.setup_layout(
    'horizontal1', central_widget, output_area,
    lambda: R_xlsx2csv(window, output_area),
    lambda: R_rename_csv(window, output_area),
    lambda: R_conv_module(window, output_area),
    lambda: R_mks2chain(window, output_area),
    lambda: R_split_chg(window, output_area),
    lambda: R_insert_chg(window, output_area),
    lambda: R_clean_csv(window, output_area),
    lambda: R_mkcc(window, output_area),
    lambda: R_proc_module(window, output_area),
    lambda: R_get_virt_end(window, output_area),
    lambda: R_virt_start(window, output_area),
    lambda: R_virt_end(window, output_area),
    lambda: R_upd_virt_end(window, output_area),
    lambda: R_combine_txt(window, output_area),
    lambda: R_virt_sect_mod(window, output_area)
)
horizontal_layout_action = layout_menu.addAction('Horizontal Layout')
horizontal_layout_action.setShortcut(QKeySequence('Ctrl+Alt+K'))
vertical_layout_action = layout_menu.addAction('Vertical Layout')
vertical_layout_action.setShortcut(QKeySequence('Ctrl+Alt+J'))
horizontal_left_layout_action = layout_menu.addAction('Horizontal left Layout')
vertical_top_layout_action = layout_menu.addAction('Vertical top Layout')
horizontal_layout_action.triggered.connect(
    lambda: layout_plugin.set_horizontal_layout(
        central_widget, output_area,
        lambda: R_xlsx2csv(window, output_area),
        lambda: R_rename_csv(window, output_area),
        lambda: R_conv_module(window, output_area),
        lambda: R_mks2chain(window, output_area),
        lambda: R_split_chg(window, output_area),
        lambda: R_insert_chg(window, output_area),
        lambda: R_clean_csv(window, output_area),
        lambda: R_mkcc(window, output_area),
        lambda: R_proc_module(window, output_area),
        lambda: R_get_virt_end(window, output_area),
        lambda: R_virt_start(window, output_area),
        lambda: R_virt_end(window, output_area),
        lambda: R_upd_virt_end(window, output_area),
        lambda: R_combine_txt(window, output_area),
        lambda: R_virt_sect_mod(window, output_area)
    )
)
vertical_layout_action.triggered.connect(
    lambda: layout_plugin.set_vertical_layout(
        central_widget, output_area,
        lambda: R_xlsx2csv(window, output_area),
        lambda: R_rename_csv(window, output_area),
        lambda: R_conv_module(window, output_area),
        lambda: R_mks2chain(window, output_area),
        lambda: R_split_chg(window, output_area),
        lambda: R_insert_chg(window, output_area),
        lambda: R_clean_csv(window, output_area),
        lambda: R_mkcc(window, output_area),
        lambda: R_proc_module(window, output_area),
        lambda: R_get_virt_end(window, output_area),
        lambda: R_virt_start(window, output_area),
        lambda: R_virt_end(window, output_area),
        lambda: R_upd_virt_end(window, output_area),
        lambda: R_combine_txt(window, output_area),
        lambda: R_virt_sect_mod(window, output_area)
    )
)
horizontal_left_layout_action.triggered.connect(
    lambda: layout_plugin.set_horizontal_left_layout(
        central_widget, output_area,
        lambda: R_xlsx2csv(window, output_area),
        lambda: R_rename_csv(window, output_area),
        lambda: R_conv_module(window, output_area),
        lambda: R_mks2chain(window, output_area),
        lambda: R_split_chg(window, output_area),
        lambda: R_insert_chg(window, output_area),
        lambda: R_clean_csv(window, output_area),
        lambda: R_mkcc(window, output_area),
        lambda: R_proc_module(window, output_area),
        lambda: R_get_virt_end(window, output_area),
        lambda: R_virt_start(window, output_area),
        lambda: R_virt_end(window, output_area),
        lambda: R_upd_virt_end(window, output_area),
        lambda: R_combine_txt(window, output_area),
        lambda: R_virt_sect_mod(window, output_area)
    )
)
vertical_top_layout_action.triggered.connect(
    lambda: layout_plugin.set_vertical_top_layout(
        central_widget, output_area,
        lambda: R_xlsx2csv(window, output_area),
        lambda: R_rename_csv(window, output_area),
        lambda: R_conv_module(window, output_area),
        lambda: R_mks2chain(window, output_area),
        lambda: R_split_chg(window, output_area),
        lambda: R_insert_chg(window, output_area),
        lambda: R_clean_csv(window, output_area),
        lambda: R_mkcc(window, output_area),
        lambda: R_proc_module(window, output_area),
        lambda: R_get_virt_end(window, output_area),
        lambda: R_virt_start(window, output_area),
        lambda: R_virt_end(window, output_area),
        lambda: R_upd_virt_end(window, output_area),
        lambda: R_combine_txt(window, output_area),
        lambda: R_virt_sect_mod(window, output_area)
    )
)
load_plugin_config()
window.show()
sys.exit(app.exec())
