# mike_gui.py
from PyQt6.QtGui import QKeySequence
import sys
from PyQt6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox,
                             QTextEdit, QHBoxLayout, QMenuBar, QMainWindow, QDialog, QLabel, QLineEdit, QKeySequenceEdit)
from script_executor import (R_xlsx2csv, R_rename_csv, R_mks2chain, R_split_chg,
                             R_insert_chg, R_clean_csv, R_mkcc, R_get_virt_end, R_virt_start, R_virt_end,
                             R_upd_virt_end, R_combine_txt, R_conv_module, R_proc_module, R_virt_sect_mod)
import theme_manager
import layout_manager
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('MIKE Easy Section Converter')
central_widget = QWidget()  # Central widget for QMainWindow
window.setCentralWidget(central_widget)
output_area = QTextEdit()
output_area.setReadOnly(True)
menu_bar = window.menuBar()
layout_menu = menu_bar.addMenu('Layout')
output_area = QTextEdit()
output_area.setReadOnly(True)

layout_manager.setup_layout(
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
horizontal_layout_action = layout_menu.addAction('Horizontal Layout')
horizontal_layout_action.setShortcut(QKeySequence('Ctrl+Alt+K'))
vertical_layout_action = layout_menu.addAction('Vertical Layout')
vertical_layout_action.setShortcut(QKeySequence('Ctrl+Alt+J'))
theme_menu = menu_bar.addMenu('Themes')
horizontal_layout_action.triggered.connect(
    lambda: layout_manager.set_horizontal_layout(
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
    lambda: layout_manager.set_vertical_layout(
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
theme_manager.create_theme_actions(window, theme_menu)
theme_manager.set_default_theme(window)
window.show()
sys.exit(app.exec())
