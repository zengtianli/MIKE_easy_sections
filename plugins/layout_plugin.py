# layout_plugin.py
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QMessageBox
from PyQt6.QtGui import QKeySequence
from plugins.layouts import layout_v, layout_h, layout_v1, layout_h1
from PyQt6 import sip
def clear_layout(layout, output_area):
    if layout is not None:
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                if widget != output_area:
                    widget.deleteLater()
                else:
                    widget.setParent(None)
            elif item.layout():
                clear_layout(item.layout(), output_area)
        sip.delete(layout)
def setup_layout(layout_type, central_widget, output_area, run_xlsx_to_csv_script, run_csv_rename_script, run_conversion_module, 
                 run_mks2chainage_script, run_chg_split, run_chg_insert, run_clean_csv, run_mkcc, run_processing_module, 
                 run_get_virtual_end, run_virtual_start, run_virtual_end, run_virtual_end_update, run_combine_files, run_virtual_section_module):
    clear_layout(central_widget.layout(), output_area)
    if layout_type == 'horizontal':
        main_layout = QVBoxLayout()
        layout_module = layout_h
    elif layout_type == 'horizontal1':
        main_layout = QVBoxLayout()
        layout_module = layout_h1
    elif layout_type == 'vertical1':
        main_layout = QHBoxLayout()
        layout_module = layout_v1
    else:  # 'vertical'
        main_layout = QHBoxLayout()
        layout_module = layout_v



    conversion_layout = layout_module.create_conversion_layout(run_xlsx_to_csv_script, run_csv_rename_script, run_conversion_module, run_mks2chainage_script)
    processing_layout = layout_module.create_processing_layout(run_chg_split, run_chg_insert, run_clean_csv, run_mkcc, run_processing_module)
    virtual_section_layout = layout_module.create_virtual_section_layout(run_get_virtual_end, run_virtual_start, run_virtual_end, run_virtual_end_update, run_combine_files, run_virtual_section_module)
    for layout in [conversion_layout, processing_layout, virtual_section_layout]:
        wrapper = QWidget()
        wrapper.setLayout(layout)
        main_layout.addWidget(wrapper)
    main_layout.addWidget(output_area)
    central_widget.setLayout(main_layout)
def set_horizontal_layout(central_widget, output_area, *args):
    setup_layout('horizontal', central_widget, output_area, *args)
def set_vertical_layout(central_widget, output_area, *args):
    setup_layout('vertical', central_widget, output_area, *args)
def set_horizontal_left_layout(central_widget, output_area, *args):
    setup_layout('horizontal1', central_widget, output_area, *args)
def set_vertical_top_layout(central_widget, output_area, *args):
    setup_layout('vertical1', central_widget, output_area, *args)