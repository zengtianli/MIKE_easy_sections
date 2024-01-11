# layout_manager.py
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QMainWindow, QTextEdit

# Import the script_executor functions and the layout_plugin
from script_executor import (R_xlsx2csv, R_rename_csv, R_mks2chain, R_split_chg,
                             R_insert_chg, R_clean_csv, R_mkcc, R_get_virt_end, R_virt_start, R_virt_end,
                             R_upd_virt_end, R_combine_txt, R_conv_module, R_proc_module, R_virt_sect_mod)
from plugins import layout_plugin

def setup_layout_menus(layout_menu, window: QMainWindow, central_widget, output_area: QTextEdit):
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

