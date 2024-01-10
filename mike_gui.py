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
def load_plugin(plugin_file):
    plugin_path = os.path.join(plugins_folder, plugin_file)
    if os.path.isfile(plugin_path) and plugin_file.endswith('.py'):
        spec = importlib.util.spec_from_file_location(
            "plugin_module", plugin_path)
        plugin_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin_module)
        if hasattr(plugin_module, 'Plugin'):
            plugin = plugin_module.Plugin()
            plugin.initialize(window, menu_bar)
def open_plugin_selection():
    dialog = PluginSelectionDialog(plugins_folder, window)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        selected_plugin_file = dialog.selected_plugin()
        if selected_plugin_file:
            load_plugin(selected_plugin_file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
plugins_folder = os.path.join(BASE_DIR, 'plugins')
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('MIKE Easy Section Converter')
central_widget = QWidget()  # Central widget for QMainWindow
window.setCentralWidget(central_widget)
output_area = QTextEdit()
output_area.setReadOnly(True)
menu_bar = window.menuBar()
# layout_menu = menu_bar.addMenu('Layout')

output_area = QTextEdit()
output_area.setReadOnly(True)
plugins_menu = menu_bar.addMenu('Plugins')
plugin_selection_action = plugins_menu.addAction('Load Plugin')
plugin_selection_action.triggered.connect(open_plugin_selection)

layout_plugin.setup_layout(
    'vertical', central_widget, output_area,
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

# horizontal_layout_action = layout_menu.addAction('Horizontal Layout')
# horizontal_layout_action.setShortcut(QKeySequence('Ctrl+Alt+K'))
# vertical_layout_action = layout_menu.addAction('Vertical Layout')
# vertical_layout_action.setShortcut(QKeySequence('Ctrl+Alt+J'))

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
window.show()
sys.exit(app.exec())
