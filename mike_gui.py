import sys, os, glob
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
def set_theme(theme_file):
    theme_folder = os.path.join(BASE_DIR, 'themes')
    theme_path = os.path.join(theme_folder, theme_file)
    with open(theme_path, 'r') as f:
        style_sheet = f.read()
    window.setStyleSheet(style_sheet)
def set_modern_apple_light_theme():
    set_theme('ModernAppleLightWithAccent.qss')
def set_apple_dark_light_hybrid_theme():
    set_theme('AppleDarkLightHybrid.qss')
def set_classic_apple_light_theme():
    set_theme('ClassicAppleLight.qss')
def set_elegant_dark_theme():
    set_theme('ElegantDarkTheme.qss')
def set_soft_blue_theme():
    set_theme('SoftBlueTheme.qss')
def set_minimalist_green_theme():
    set_theme('MinimalistGreenTheme.qss')
def set_warm_sunset_theme():
    set_theme('WarmSunsetTheme.qss')
def set_retrowave_theme():
    set_theme('RetroWaveTheme.qss')
def set_nature_inspired_theme():
    set_theme('NatureInspiredTheme.qss')
def set_tech_professional_theme():
    set_theme('TechProfessionalTheme.qss')
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
    execute_script(
        xlsx2csv_all.main,
        "XLSX to <u>CSV</u> conversion completed!",
        "Error occurred during conversion"
    )
'world'
def run_csv_rename_script():
    execute_script(
        csv_rn_cap.main,
        "CSV file renaming completed!",
        "Error occurred during renaming"
    )
def run_mks2chainage_script():
    input_file_path = os.path.join(BASE_DIR, 'secss.txt')
    execute_script(
        mks2chainage.main,
        "according to MIKE section file(txt) generate a mileage csv completed, saved as <u>chainage.csv</u> (need modify manually)!",
        "Error occurred during mks2chainage script execution",
        input_file_path
    )
def run_chg_split():
    execute_script(
        chg_split.main,
        "Section split according to chainage.csv file completed! Saved in <u>chg_files</u> folder!",
        "Error occurred during chg_split script execution"
    )
def run_chg_insert():
    execute_script(
        chg_insert.main,
        "Insertion of related section information from chg_files into corresponding files ! Saved in <u>inserted_files</u> folder!",
        "Error occurred during chg_insert script execution"
    )
def run_clean_csv():
    execute_script(
        clean_csv.main,
        "clean csv data completed! Saved in <u>cleaned_files</u> folder!",
        "Error occurred during clean_csv script execution"
    )
def run_mkcc():
    execute_script(
        mkcc.main,
        "according to csv files generate MIKE section file(txt) completed! Saved in <u>txt_files</u> folder!",
        "Error occurred during mkcc script execution"
    )
def run_get_virtual_end():
    execute_script(
        get_virtual_end.main,
        "Extract virtual section from chg_files and combine them into <u>all_virtual_end.csv </u>",
        "Error occurred during get_virtual_end script execution"
    )
def run_virtual_start():
    execute_script(
        virtual_start.main,
        "add start virtual section to txt files, save in  <u>txt_virtual_start</u> folder! ",
        "Error occurred during virtual_start script execution"
    )
def run_virtual_end():
    execute_script(
        virtual_end.main,
        "add end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!",
        "Error occurred during virtual_end script execution"
    )
def run_virtual_end_update():
    execute_script(
        virtual_end_update.main,
        "update end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!",
        "Error occurred during virtual_end_update script execution"
    )
def run_combine_files():
    execute_script(
        combine_files,
        "Combine all txt files into <u>combined.txt</u> file!",
        "Error occurred during combine_files script execution"
    )
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
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('MIKE Easy Section Converter')
central_widget = QWidget()  # Central widget for QMainWindow
window.setCentralWidget(central_widget)
main_layout = QHBoxLayout(central_widget)
menu_bar = window.menuBar()
theme_menu = menu_bar.addMenu('Themes')
Theme_modern_apple_light_action = theme_menu.addAction('Modern Apple Light')
Theme_apple_dark_light_hybrid_action = theme_menu.addAction('Apple Dark Light Hybrid')
Theme_classic_apple_light_action = theme_menu.addAction('Classic Apple Light')
Theme_elegant_dark_action = theme_menu.addAction('Elegant Dark')
Theme_soft_blue_action = theme_menu.addAction('Soft Blue')
Theme_minimalist_green_action = theme_menu.addAction('Minimalist Green')
Theme_warm_sunset_action = theme_menu.addAction('Warm Sunset')
Theme_retrowave_action = theme_menu.addAction('Retro Wave')
Theme_nature_inspired_action = theme_menu.addAction('Nature Inspired')
Theme_tech_professional_action = theme_menu.addAction('Tech Professional')
Theme_modern_apple_light_action.triggered.connect(set_modern_apple_light_theme)
Theme_apple_dark_light_hybrid_action.triggered.connect(set_apple_dark_light_hybrid_theme)
Theme_classic_apple_light_action.triggered.connect(set_classic_apple_light_theme)
Theme_elegant_dark_action.triggered.connect(set_elegant_dark_theme)
Theme_soft_blue_action.triggered.connect(set_soft_blue_theme)
Theme_minimalist_green_action.triggered.connect(set_minimalist_green_theme)
Theme_warm_sunset_action.triggered.connect(set_warm_sunset_theme)
Theme_retrowave_action.triggered.connect(set_retrowave_theme)
Theme_nature_inspired_action.triggered.connect(set_nature_inspired_theme)
Theme_tech_professional_action.triggered.connect(set_tech_professional_theme)
conversion_layout = QVBoxLayout()
con_xlsx_to_csv_button = QPushButton('XLSX to CSV')
con_csv_rename_button = QPushButton('Rename CSV')
conversion_layout.addWidget(con_xlsx_to_csv_button)
conversion_layout.addWidget(con_csv_rename_button)
# Processing Module Layout
processing_layout = QVBoxLayout()
pro_mks2chainage_button = QPushButton('MIKE to Chainage CSV')
pro_chg_split_button = QPushButton('Split Chainage Sections')
pro_chg_insert_button = QPushButton('Insert Section Data')
pro_clean_csv_button = QPushButton('Clean CSV Data')
pro_mkcc_button = QPushButton('Run MKCC')
processing_layout.addWidget(pro_mks2chainage_button)
processing_layout.addWidget(pro_chg_split_button)
processing_layout.addWidget(pro_chg_insert_button)
processing_layout.addWidget(pro_clean_csv_button)
processing_layout.addWidget(pro_mkcc_button)
# Virtual Section Management Module Layout
virtual_section_layout = QVBoxLayout()
virtual_get_end_button = QPushButton('Get Virtual End')
virtual_start_button = QPushButton('Set Virtual Start')
virtual_end_button = QPushButton('Set Virtual End')
virtual_end_update_button = QPushButton('Update Virtual End')
vir_combine_files_button = QPushButton('Combine Files')
virtual_section_layout.addWidget(virtual_get_end_button)
virtual_section_layout.addWidget(virtual_start_button)
virtual_section_layout.addWidget(virtual_end_button)
virtual_section_layout.addWidget(virtual_end_update_button)
virtual_section_layout.addWidget(vir_combine_files_button)
# Add stretch to push the module buttons down
conversion_layout.addStretch()
processing_layout.addStretch()
virtual_section_layout.addStretch()
# Module buttons
conversion_module_button = QPushButton('Conversion Module')
processing_module_button = QPushButton('Processed Data Module')
virtual_section_module_button = QPushButton('Virtual Section Module')
# Add module buttons to the layouts
conversion_layout.addWidget(conversion_module_button)
processing_layout.addWidget(processing_module_button)
virtual_section_layout.addWidget(virtual_section_module_button)
# Add layouts to the main layout
main_layout.addLayout(conversion_layout)
main_layout.addLayout(processing_layout)
main_layout.addLayout(virtual_section_layout)
# Output Area
output_area = QTextEdit()
output_area.setReadOnly(True)
main_layout.addWidget(output_area)
# Connect buttons to their respective functions
con_xlsx_to_csv_button.clicked.connect(run_xlsx_to_csv_script)
con_csv_rename_button.clicked.connect(run_csv_rename_script)
conversion_module_button.clicked.connect(run_conversion_module)
pro_mks2chainage_button.clicked.connect(run_mks2chainage_script)
pro_chg_split_button.clicked.connect(run_chg_split)
pro_chg_insert_button.clicked.connect(run_chg_insert)
pro_clean_csv_button.clicked.connect(run_clean_csv)
pro_mkcc_button.clicked.connect(run_mkcc)
processing_module_button.clicked.connect(run_processing_module)
virtual_get_end_button.clicked.connect(run_get_virtual_end)
virtual_start_button.clicked.connect(run_virtual_start)
virtual_end_button.clicked.connect(run_virtual_end)
virtual_end_update_button.clicked.connect(run_virtual_end_update)
vir_combine_files_button.clicked.connect(run_combine_files)
virtual_section_module_button.clicked.connect(run_virtual_section_module)
window.show()
sys.exit(app.exec())
