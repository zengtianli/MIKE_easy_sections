import sys, os, glob,layout_v,layout_h
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit, QHBoxLayout, QMenuBar, QMainWindow
import xlsx2csv_all, csv_rn_cap, mks2chainage, chg_split, chg_insert, clean_csv, get_virtual_end, virtual_start, mkcc, virtual_end, virtual_end_update
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

def combine_files():
    if os.path.isfile('./processed_data/combined.txt'):
        os.remove('./processed_data/combined.txt')
    with open('./combined.txt', 'w') as outfile:
        for filename in glob.glob('./processed_data/txt_virtual_end/*.txt'):
            with open(filename, 'r') as readfile:
                outfile.write(readfile.read())
class EmittingStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, message):
        self.text_widget.append(message)
    def flush(self):
        pass


def execute_script(script_func, success_message, error_message, *args):
    sys.stdout = EmittingStream(output_area)
    try:
        if args:
            script_func(*args)
        else:
            script_func()
        QMessageBox.information(window, "Completed", success_message)
    except Exception as e:
        QMessageBox.critical(window, "Error", f"{error_message}: {e}")
    finally:
        sys.stdout = sys.__stdout__
def run_xlsx_to_csv_script():
    xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    execute_script( xlsx2csv_all.main, "XLSX to <u>CSV</u> conversion completed!", "Error occurred during conversion")
def run_csv_rename_script():
    execute_script( csv_rn_cap.main, "CSV file renaming completed!", "Error occurred during renaming")
def run_mks2chainage_script():
    input_file_path = os.path.join(BASE_DIR, 'secss.txt')
    execute_script( mks2chainage.main, "according to MIKE section file(txt) generate a mileage csv completed, saved as <u>chainage.csv</u> (need modify manually)!", "Error occurred during mks2chainage script execution", input_file_path)
def run_chg_split():
    execute_script( chg_split.main, "Section split according to chainage.csv file completed! Saved in <u>chg_files</u> folder!", "Error occurred during chg_split script execution")
def run_chg_insert():
    execute_script( chg_insert.main, "Insertion of related section information from chg_files into corresponding files ! Saved in <u>inserted_files</u> folder!", "Error occurred during chg_insert script execution")
def run_clean_csv():
    execute_script( clean_csv.main, "clean csv data completed! Saved in <u>cleaned_files</u> folder!", "Error occurred during clean_csv script execution")
def run_mkcc():
    execute_script( mkcc.main, "according to csv files generate MIKE section file(txt) completed! Saved in <u>txt_files</u> folder!", "Error occurred during mkcc script execution")
def run_get_virtual_end():
    execute_script( get_virtual_end.main, "Extract virtual section from chg_files and combine them into <u>all_virtual_end.csv </u>", "Error occurred during get_virtual_end script execution")
def run_virtual_start():
    execute_script( virtual_start.main, "add start virtual section to txt files, save in  <u>txt_virtual_start</u> folder! ", "Error occurred during virtual_start script execution")
def run_virtual_end():
    execute_script( virtual_end.main, "add end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!", "Error occurred during virtual_end script execution")
def run_virtual_end_update():
    execute_script( virtual_end_update.main, "update end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!", "Error occurred during virtual_end_update script execution")
def run_combine_files():
    execute_script( combine_files, "Combine all txt files into <u>combined.txt</u> file!", "Error occurred during combine_files script execution")
# Conversion Module Function
def run_conversion_module():
    run_xlsx_to_csv_script()
    run_csv_rename_script()
# Processing Module Function
def run_processing_module():
    run_mks2chainage_script()
    run_chg_split()
    run_chg_insert()
    run_clean_csv()
    run_mkcc()
# Virtual Section Management Module Function
def run_virtual_section_module():
    run_get_virtual_end()
    run_virtual_start()
    run_virtual_end()
    run_virtual_end_update()
    run_combine_files()
def set_horizontal_layout():
    clear_layout(main_layout)
    setup_layout('horizontal')
from PyQt6 import sip
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('MIKE Easy Section Converter')
central_widget = QWidget()  # Central widget for QMainWindow
window.setCentralWidget(central_widget)
output_area = QTextEdit()
output_area.setReadOnly(True)
def clear_layout(layout):
    if layout is not None:
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                if widget != output_area:  # Make sure not to delete output_area
                    widget.deleteLater()
                else:
                    widget.setParent(None)  # Reparent output_area to keep it alive
            elif item.layout():
                # Recursively clear sublayouts
                clear_layout(item.layout())
        sip.delete(layout)
def setup_layout(layout_type):
    global central_widget, output_area
    # clear_layout(central_widget)
    clear_layout(central_widget.layout())
    # Creating new instances of the layouts
    if layout_type == 'horizontal':
        main_layout = QVBoxLayout()
        conversion_layout = layout_h.create_conversion_layout(run_xlsx_to_csv_script, run_csv_rename_script, run_conversion_module)
        processing_layout = layout_h.create_processing_layout(run_mks2chainage_script, run_chg_split, run_chg_insert, run_clean_csv, run_mkcc, run_processing_module)
        virtual_section_layout = layout_h.create_virtual_section_layout(run_get_virtual_end, run_virtual_start, run_virtual_end, run_virtual_end_update, run_combine_files, run_virtual_section_module)
    else:  # 'vertical'
        main_layout = QHBoxLayout()
        conversion_layout = layout_v.create_conversion_layout(run_xlsx_to_csv_script, run_csv_rename_script, run_conversion_module)
        processing_layout = layout_v.create_processing_layout(run_mks2chainage_script, run_chg_split, run_chg_insert, run_clean_csv, run_mkcc, run_processing_module)
        virtual_section_layout = layout_v.create_virtual_section_layout(run_get_virtual_end, run_virtual_start, run_virtual_end, run_virtual_end_update, run_combine_files, run_virtual_section_module)
    # Add the new instances to the main layout
    for layout in [conversion_layout, processing_layout, virtual_section_layout]:
        if isinstance(main_layout, QVBoxLayout):
            main_layout.addLayout(layout)
        else:
            widget_wrapper = QWidget()  # A new wrapper widget for the horizontal layout
            widget_wrapper.setLayout(layout)
            main_layout.addWidget(widget_wrapper)
    main_layout.addWidget(output_area)
    central_widget.setLayout(main_layout)
def set_horizontal_layout(): setup_layout('horizontal')
def set_vertical_layout(): setup_layout('vertical')
setup_layout('vertical')

menu_bar = window.menuBar()
layout_menu = menu_bar.addMenu('Layout')
theme_menu = menu_bar.addMenu('Themes')

horizontal_layout_action = layout_menu.addAction('Horizontal Layout')
vertical_layout_action = layout_menu.addAction('Vertical Layout')
horizontal_layout_action.triggered.connect(set_horizontal_layout)
vertical_layout_action.triggered.connect(set_vertical_layout)

from PyQt6.QtGui import QKeySequence

# ...

horizontal_layout_action = layout_menu.addAction('Horizontal Layout')
horizontal_layout_action.setShortcut(QKeySequence('Ctrl+Alt+C')) 
horizontal_layout_action.triggered.connect(set_horizontal_layout)

vertical_layout_action = layout_menu.addAction('Vertical Layout')
vertical_layout_action.setShortcut(QKeySequence('Ctrl+Alt+V'))  
vertical_layout_action.triggered.connect(set_vertical_layout)


import theme_manager
theme_manager.create_theme_actions(window, theme_menu)
theme_manager.set_default_theme(window)
window.show()
sys.exit(app.exec())
