# layout_plugin.py
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QTextEdit
from plugin_interface import PluginInterface
from script_executor import (R_xlsx2csv, R_rename_csv, R_mks2chain, R_split_chg,
                             R_insert_chg, R_clean_csv, R_mkcc, R_get_virt_end, R_virt_start, R_virt_end,
                             R_upd_virt_end, R_combine_txt, R_conv_module, R_proc_module, R_virt_sect_mod)
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QMessageBox
from plugins.layouts import layout_v, layout_h, layout_v1, layout_h1
from PyQt6 import sip
import os,json
from constants import PLUGIN_CONFIG_FILE
class Plugin(PluginInterface):
    def initialize(self, window: QMainWindow, menu):
        self.window = window
        self.create_layout_menu(menu)
    def create_layout_menu(self, menu):
        layout_menu = menu.addMenu('Layout')
        self.create_layout_actions(layout_menu, self.window.centralWidget(), self.window.output_area)
    def clear_layout(self, layout, output_area):
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
                    self.clear_layout(item.layout(), output_area)
            sip.delete(layout)
    def setup_layout(self,layout_type, central_widget, output_area, run_xlsx_to_csv_script, run_csv_rename_script, run_conversion_module, run_mks2chainage_script, run_chg_split, run_chg_insert, run_clean_csv, run_mkcc, run_processing_module, run_get_virtual_end, run_virtual_start, run_virtual_end, run_virtual_end_update, run_combine_files, run_virtual_section_module):
        self.clear_layout(central_widget.layout(), output_area)
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
        self.save_config(layout_type)
    def get_script_actions(self, output_area):
        return {
            'xlsx_to_csv': lambda: R_xlsx2csv(self.window, output_area),
            'rename_csv': lambda: R_rename_csv(self.window, output_area),
            'conversion_module': lambda: R_conv_module(self.window, output_area),
            'mks2chainage': lambda: R_mks2chain(self.window, output_area),
            'chg_split': lambda: R_split_chg(self.window, output_area),
            'chg_insert': lambda: R_insert_chg(self.window, output_area),
            'clean_csv': lambda: R_clean_csv(self.window, output_area),
            'mkcc': lambda: R_mkcc(self.window, output_area),
            'processing_module': lambda: R_proc_module(self.window, output_area),
            'get_virtual_end': lambda: R_get_virt_end(self.window, output_area),
            'virtual_start': lambda: R_virt_start(self.window, output_area),
            'virtual_end': lambda: R_virt_end(self.window, output_area),
            'virtual_end_update': lambda: R_upd_virt_end(self.window, output_area),
            'combine_files': lambda: R_combine_txt(self.window, output_area),
            'virtual_section_module': lambda: R_virt_sect_mod(self.window, output_area)
            }
    def setup_layout(self, layout_type, central_widget, output_area, script_actions):
        self.clear_layout(central_widget.layout(), output_area)
        # Determine the layout module based on the layout_type
        layout_module = {
            'horizontal': layout_h,
            'horizontal1': layout_h1,
            'vertical': layout_v,
            'vertical1': layout_v1
        }.get(layout_type, layout_v)  # Default to vertical if not found
        main_layout = QVBoxLayout() if 'horizontal' in layout_type else QHBoxLayout()
        conversion_layout = layout_module.create_conversion_layout(
            script_actions['xlsx_to_csv'], 
            script_actions['rename_csv'], 
            script_actions['mks2chainage'],
            script_actions['conversion_module'], 
        )
        processing_layout = layout_module.create_processing_layout(
            script_actions['chg_split'],
            script_actions['chg_insert'],
            script_actions['clean_csv'],
            script_actions['mkcc'],
            script_actions['processing_module'],
        )
        virtual_section_layout = layout_module.create_virtual_section_layout(
            script_actions['get_virtual_end'],
            script_actions['virtual_start'],
            script_actions['virtual_end'],
            script_actions['virtual_end_update'],
            script_actions['combine_files'],
            script_actions['virtual_section_module'],
        )
        for layout in [conversion_layout, processing_layout, virtual_section_layout]:
            wrapper = QWidget()
            wrapper.setLayout(layout)
            main_layout.addWidget(wrapper)
        main_layout.addWidget(output_area)
        central_widget.setLayout(main_layout)
        self.save_config(layout_type)
    def set_horizontal_layout(self, central_widget, output_area):
        script_actions = self.get_script_actions(output_area)
        self.setup_layout('horizontal', central_widget, output_area, script_actions)
    def set_vertical_layout(self, central_widget, output_area):
        script_actions = self.get_script_actions(output_area)
        self.setup_layout('vertical', central_widget, output_area, script_actions)
    # set_horizontal_left_layout like above
    def set_horizontal_left_layout(self, central_widget, output_area):
        script_actions = self.get_script_actions(output_area)
        self.setup_layout('horizontal1', central_widget, output_area, script_actions)
    def set_vertical_top_layout(self, central_widget, output_area):
        script_actions = self.get_script_actions(output_area)
        self.setup_layout('vertical1', central_widget, output_area, script_actions)
    def deinitialize(self, window, menu):
        for action in menu.actions():
            if action.text() == 'Layout':
                menu.removeAction(action)
                break
    def create_layout_actions(self, layout_menu, central_widget, output_area):
        horizontal_layout_action = QAction('Horizontal Layout', self.window)
        horizontal_layout_action.triggered.connect(
            lambda: self.set_horizontal_layout(central_widget, output_area)
        )
        layout_menu.addAction(horizontal_layout_action)
        horizontal_left_layout_action = QAction('Horizontal Left Layout', self.window)
        horizontal_left_layout_action.triggered.connect(
            lambda: self.set_horizontal_left_layout(central_widget, output_area)
        )
        layout_menu.addAction(horizontal_left_layout_action)
        vertical_layout_action = QAction('Vertical Layout', self.window)
        vertical_layout_action.triggered.connect(
            lambda: self.set_vertical_layout(central_widget, output_area)
        )
        layout_menu.addAction(vertical_layout_action)
        vertical_top_layout_action = QAction('Vertical Top Layout', self.window)
        vertical_top_layout_action.triggered.connect(
            lambda: self.set_vertical_top_layout(central_widget, output_area)
        )
        layout_menu.addAction(vertical_top_layout_action)
    def save_config(self, layout_type):
        config_key = 'layout_plugin'  # Plugin name without .py
        config = {}
        if os.path.exists(PLUGIN_CONFIG_FILE):
            with open(PLUGIN_CONFIG_FILE, 'r') as file:
                config = json.load(file)
        config[config_key] = {'saved_setting': layout_type}
        with open(PLUGIN_CONFIG_FILE, 'w') as file:
            json.dump(config, file)
    def load_settings(self, settings):
        if 'saved_setting' in settings:
            saved_layout_type = settings['saved_setting']
            script_actions = self.get_script_actions(self.window.output_area)
            if saved_layout_type == 'horizontal':
                self.set_horizontal_layout(self.window.centralWidget(), self.window.output_area)
            elif saved_layout_type == 'vertical':
                self.set_vertical_layout(self.window.centralWidget(), self.window.output_area)
            elif saved_layout_type == 'horizontal1':
                self.set_horizontal_left_layout(self.window.centralWidget(), self.window.output_area)
            elif saved_layout_type == 'vertical1':
                self.set_vertical_top_layout(self.window.centralWidget(), self.window.output_area)
