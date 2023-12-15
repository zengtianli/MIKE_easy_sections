import sys, os, glob
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit, QHBoxLayout

import xlsx2csv_all, csv_rn_cap, mks2chainage, chg_split, chg_insert, clean_csv, get_virtual_end, virtual_start, mkcc, virtual_end, virtual_end_update

# Import your scripts here
import xlsx2csv_all, csv_rn_cap, mks2chainage, chg_split, chg_insert, clean_csv, get_virtual_end, virtual_start, mkcc, virtual_end, virtual_end_update

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
def combine_files():
    if os.path.isfile('./processed_data/combined.txt'):
        os.remove('./processed_data/combined.txt')
    with open('./combined.txt', 'w') as outfile:
        for filename in glob.glob('./processed_data/txt_updated_files/*.txt'):
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
    execute_script(
        xlsx2csv_all.main,
        "XLSX to CSV conversion completed!",
        "Error occurred during conversion"
    )

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
        "MIKE section file conversion to mileage csv completed, saved as chainage.csv!",
        "Error occurred during mks2chainage script execution",
        input_file_path
    )

def run_chg_split():
    execute_script(
        chg_split.main,
        "Section split according to chainage.csv file completed! Saved in chg_files folder!",
        "Error occurred during chg_split script execution"
    )

def run_chg_insert():
    execute_script(
        chg_insert.main,
        "Insertion of related section information into corresponding files from chg_files completed! Saved in inserted_files folder!",
        "Error occurred during chg_insert script execution"
    )

def run_clean_csv():
    execute_script(
        clean_csv.main,
        "Insertion of related section information into corresponding files from chg_files completed! Saved in inserted_files folder!",
        "Error occurred during clean_csv script execution"
    )

def run_mkcc():
    execute_script(
        mkcc.main,
        "Insertion of related section information into corresponding files from chg_files completed! Saved in inserted_files folder!",
        "Error occurred during mkcc script execution"
    )

def run_get_virtual_end():
    execute_script(
        get_virtual_end.main,
        "Extraction of virtual section mileage completed! Saved in processed_data folder!",
        "Error occurred during get_virtual_end script execution"
    )

def run_virtual_start():
    execute_script(
        virtual_start.main,
        "Extraction of virtual section mileage completed! Saved in processed_data folder!",
        "Error occurred during virtual_start script execution"
    )

def run_virtual_end():
    execute_script(
        virtual_end.main,
        "Extraction of virtual section mileage completed! Saved in processed_data folder!",
        "Error occurred during virtual_end script execution"
    )

def run_virtual_end_update():
    execute_script(
        virtual_end_update.main,
        "Extraction of virtual section mileage completed! Saved in processed_data folder!",
        "Error occurred during virtual_end_update script execution"
    )

def run_combine_files():
    execute_script(
        combine_files,
        "Extraction of virtual section mileage completed! Saved in processed_data folder!",
        "Error occurred during combine_files script execution"
    )

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('MIKE Easy Section Converter')

# Main layout
main_layout = QHBoxLayout()
window.setLayout(main_layout)

# Conversion Module Layout
conversion_layout = QVBoxLayout()
xlsx_to_csv_button = QPushButton('XLSX to CSV')
csv_rename_button = QPushButton('Rename CSV')
conversion_layout.addWidget(xlsx_to_csv_button)
conversion_layout.addWidget(csv_rename_button)
main_layout.addLayout(conversion_layout)

# Processing Module Layout
processing_layout = QVBoxLayout()
mks2chainage_button = QPushButton('MIKE to Chainage CSV')
chg_split_button = QPushButton('Split Chainage Sections')
chg_insert_button = QPushButton('Insert Section Data')
clean_csv_button = QPushButton('Clean CSV Data')
mkcc_button = QPushButton('Run MKCC')
processing_layout.addWidget(mks2chainage_button)
processing_layout.addWidget(chg_split_button)
processing_layout.addWidget(chg_insert_button)
processing_layout.addWidget(clean_csv_button)
processing_layout.addWidget(mkcc_button)
main_layout.addLayout(processing_layout)

# Virtual Section Management Module Layout
virtual_section_layout = QVBoxLayout()
get_virtual_end_button = QPushButton('Get Virtual End')
virtual_start_button = QPushButton('Set Virtual Start')
virtual_end_button = QPushButton('Set Virtual End')
virtual_end_update_button = QPushButton('Update Virtual End')
combine_files_button = QPushButton('Combine Files')
virtual_section_layout.addWidget(get_virtual_end_button)
virtual_section_layout.addWidget(virtual_start_button)
virtual_section_layout.addWidget(virtual_end_button)
virtual_section_layout.addWidget(virtual_end_update_button)
virtual_section_layout.addWidget(combine_files_button)
main_layout.addLayout(virtual_section_layout)

# Output Area
output_area = QTextEdit()
output_area.setReadOnly(True)
main_layout.addWidget(output_area)

# Connect buttons to their respective functions
xlsx_to_csv_button.clicked.connect(run_xlsx_to_csv_script)
csv_rename_button.clicked.connect(run_csv_rename_script)
mks2chainage_button.clicked.connect(run_mks2chainage_script)
chg_split_button.clicked.connect(run_chg_split)
chg_insert_button.clicked.connect(run_chg_insert)
clean_csv_button.clicked.connect(run_clean_csv)
mkcc_button.clicked.connect(run_mkcc)
get_virtual_end_button.clicked.connect(run_get_virtual_end)
virtual_start_button.clicked.connect(run_virtual_start)
virtual_end_button.clicked.connect(run_virtual_end)
virtual_end_update_button.clicked.connect(run_virtual_end_update)
combine_files_button.clicked.connect(run_combine_files)

window.show()
sys.exit(app.exec_())

