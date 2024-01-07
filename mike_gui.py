import sys,os,glob
from scripts import xlsx2csv_all, csv_rn_cap, mks2chainage, chg_split, chg_insert, clean_csv, get_virtual_end, virtual_start, mkcc, virtual_end, virtual_end_update
from PyQt6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit, QHBoxLayout, QMenuBar, QMainWindow, QDialog, QLabel, QLineEdit, QKeySequenceEdit)


BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
def combine_files():
    if os.path.isfile('./processed_data/combined.txt'):
        os.remove('./processed_data/combined.txt')
    with open('./combined.txt', 'w') as outfile:
        for filename in glob.glob('./processed_data/txt_virtual_end/*.txt'):
            with open(filename, 'r') as readfile:
                outfile.write(readfile.read())

script_mappings = {
    "xlsx_to_csv": {
        "func": xlsx2csv_all.main,
        "success_msg": "XLSX to <u>CSV</u> conversion completed!",
        "error_msg": "Error occurred during conversion"
    },
    "csv_rename": {
        "func": csv_rn_cap.main,
        "success_msg": "CSV file renaming completed!",
        "error_msg": "Error occurred during renaming"
    },
    # Add other script mappings here
    "mks2chainage": {
        "func": mks2chainage.main,
        "success_msg": "according to MIKE section file(txt) generate a mileage csv completed, saved as <u>chainage.csv</u> (need modify manually)!",
        "error_msg": "Error occurred during mks2chainage script execution"
    },
    "chg_split": {
        "func": chg_split.main,
        "success_msg": "Section split according to chainage.csv file completed! Saved in <u>chg_files</u> folder!",
        "error_msg": "Error occurred during chg_split script execution"
    },
    "chg_insert": {
        "func": chg_insert.main,
        "success_msg": "Insertion of related section information from chg_files into corresponding files ! Saved in <u>inserted_files</u> folder!",
        "error_msg": "Error occurred during chg_insert script execution"
    },
    "clean_csv": {
        "func": clean_csv.main,
        "success_msg": "clean csv data completed! Saved in <u>cleaned_files</u> folder!",
        "error_msg": "Error occurred during clean_csv script execution"
    },
    "mkcc": {
        "func": mkcc.main,
        "success_msg": "according to csv files generate MIKE section file(txt) completed! Saved in <u>txt_files</u> folder!",
        "error_msg": "Error occurred during mkcc script execution"
    },
    "get_virtual_end": {
        "func": get_virtual_end.main,
        "success_msg": "Extract virtual section from chg_files and combine them into <u>all_virtual_end.csv </u>",
        "error_msg": "Error occurred during get_virtual_end script execution"
    },
    "virtual_start": {
        "func": virtual_start.main,
        "success_msg": "add start virtual section to txt files, save in  <u>txt_virtual_start</u> folder! ",
        "error_msg": "Error occurred during virtual_start script execution"
    },
    "virtual_end": {
        "func": virtual_end.main,
        "success_msg": "add end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!",
        "error_msg": "Error occurred during virtual_end script execution"
    },
    "virtual_end_update": {
        "func": virtual_end_update.main,
        "success_msg": "update end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!",
        "error_msg": "Error occurred during virtual_end_update script execution"
    },
    "combine_files": {
        "func": combine_files,
        "success_msg": "Combine all txt files into <u>combined.txt</u> file!",
        "error_msg": "Error occurred during combine_files script execution"
    }
}

def execute_script(script_name, *args):
    script = script_mappings[script_name]
    sys.stdout = EmittingStream(output_area)
    try:
        if args:
            script["func"](*args)
        else:
            script["func"]()
        QMessageBox.information(window, "Completed", script["success_msg"])
    except Exception as e:
        QMessageBox.critical(window, "Error", f"{script['error_msg']}: {e}")
    finally:
        sys.stdout = sys.__stdout__

class EmittingStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, message):
        self.text_widget.append(message)
    def flush(self):
        pass

# def run_xlsx_to_csv_script(): xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0])); execute_script( xlsx2csv_all.main, "XLSX to <u>CSV</u> conversion completed!", "Error occurred during conversion")
def R_xlsx2csv(): xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0])); execute_script("xlsx_to_csv")
def R_rename_csv(): execute_script("csv_rename")
def R_mks2chain(): input_file_path = os.path.join(BASE_DIR, 'secss.txt'); execute_script("mks2chainage", input_file_path)
def R_split_chg(): execute_script("chg_split")
def R_insert_chg(): execute_script("chg_insert")
def R_clean_csv(): execute_script("clean_csv")
def R_mkcc(): execute_script("mkcc")
def R_get_virt_end(): execute_script("get_virtual_end")
def R_virt_start(): execute_script("virtual_start")
def R_virt_end(): execute_script("virtual_end")
def R_upd_virt_end(): execute_script("virtual_end_update")
def R_combine_txt(): execute_script("combine_files")
def R_conv_module():
    R_xlsx2csv()
    R_rename_csv()
def R_proc_module():
    R_mks2chain()
    R_split_chg()
    R_insert_chg()
    R_clean_csv()
    R_mkcc()
def R_virt_sect_mod():
    R_get_virt_end()
    R_virt_start()
    R_virt_end()
    R_upd_virt_end()
    R_combine_txt()


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('MIKE Easy Section Converter')
central_widget = QWidget()  # Central widget for QMainWindow
window.setCentralWidget(central_widget)
output_area = QTextEdit()
output_area.setReadOnly(True)

menu_bar = window.menuBar()
layout_menu = menu_bar.addMenu('Layout')
import layout_manager
layout_manager.setup_layout(
    'vertical', central_widget, output_area, 
    R_xlsx2csv, R_rename_csv, R_conv_module, 
    R_mks2chain, R_split_chg, R_insert_chg, R_clean_csv, R_mkcc, R_proc_module, 
    R_get_virt_end, R_virt_start, R_virt_end, R_upd_virt_end, R_combine_txt, R_virt_sect_mod
)

from PyQt6.QtGui import QKeySequence
horizontal_layout_action = layout_menu.addAction('Horizontal Layout')
horizontal_layout_action.setShortcut(QKeySequence('Ctrl+Alt+C')) 
vertical_layout_action = layout_menu.addAction('Vertical Layout')
vertical_layout_action.setShortcut(QKeySequence('Ctrl+Alt+V'))  

horizontal_layout_action.triggered.connect(
    lambda: layout_manager.set_horizontal_layout(
        central_widget, output_area, 
        R_xlsx2csv, R_rename_csv, R_conv_module, 
        R_mks2chain, R_split_chg, R_insert_chg, R_clean_csv, R_mkcc, R_proc_module, 
        R_get_virt_end, R_virt_start, R_virt_end, R_upd_virt_end, R_combine_txt, R_virt_sect_mod
    )
)

vertical_layout_action.triggered.connect(
    lambda: layout_manager.set_vertical_layout(
        central_widget, output_area, 
        R_xlsx2csv, R_rename_csv, R_conv_module, 
        R_mks2chain, R_split_chg, R_insert_chg, R_clean_csv, R_mkcc_exec, R_proc_module, 
        R_get_virt_end, R_virt_start, R_virt_end, R_upd_virt_end, R_combine_txt, R_virt_sect_mod
    )
)

theme_menu = menu_bar.addMenu('Themes')
import theme_manager
theme_manager.create_theme_actions(window, theme_menu)
theme_manager.set_default_theme(window)
window.show()
sys.exit(app.exec())
