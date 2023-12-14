import sys,os,glob
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
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


def run_xlsx_to_csv_script():
    xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    sys.stdout = EmittingStream(output_area)
    try:
        xlsx2csv_all.main()
        QMessageBox.information(window, "Completed",
                                "XLSX to CSV conversion completed!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during conversion: {e}")
    sys.stdout = sys.__stdout__


def run_csv_rename_script():
    sys.stdout = EmittingStream(output_area)  # Redirect output to QTextEdit
    try:
        csv_rn_cap.main()  # Directly run the main function of the CSV renaming script
        QMessageBox.information(window, "Completed",
                                "CSV file renaming completed!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during renaming: {e}")
    sys.stdout = sys.__stdout__  # Restore standard output


def run_mks2chainage_script():
    input_file_path = os.path.join(
        BASE_DIR, 'secss.txt')  # Define input file path
    sys.stdout = EmittingStream(output_area)
    try:
        mks2chainage.main(input_file_path)
        QMessageBox.information(
            window, "Completed", "MIKE section file conversion to mileage csv completed, saved as chainage.csv!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during mks2chainage script execution: {e}")
    sys.stdout = sys.__stdout__


def run_chg_split():
    sys.stdout = EmittingStream(output_area)
    try:
        chg_split.main()
        QMessageBox.information(
            window, "Completed", "Section split according to chainage.csv file completed! Saved in chg_files folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during chg_split script execution: {e}")
    sys.stdout = sys.__stdout__


def run_chg_insert():
    sys.stdout = EmittingStream(output_area)
    try:
        chg_insert.main()
        QMessageBox.information(
            window, "Completed", "Insertion of related section information into corresponding files from chg_files completed! Saved in inserted_files folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during chg_insert script execution: {e}")
    sys.stdout = sys.__stdout__


def run_clean_csv():
    sys.stdout = EmittingStream(output_area)
    try:
        clean_csv.main()
        QMessageBox.information(
            window, "Completed", "Insertion of related section information into corresponding files from chg_files completed! Saved in inserted_files folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during clean_csv script execution: {e}")
    sys.stdout = sys.__stdout__


def run_mkcc():
    sys.stdout = EmittingStream(output_area)
    try:
        mkcc.main()
        QMessageBox.information(
            window, "Completed", "Insertion of related section information into corresponding files from chg_files completed! Saved in inserted_files folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during mkcc script execution: {e}")
    sys.stdout = sys.__stdout__


def run_get_virtual_end():
    sys.stdout = EmittingStream(output_area)
    try:
        get_virtual_end.main()
        QMessageBox.information(
            window, "Completed", "Extraction of virtual section mileage completed! Saved in processed_data folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during get_virtual_end script execution: {e}")
    sys.stdout = sys.__stdout__


def run_virtual_start():
    sys.stdout = EmittingStream(output_area)
    try:
        virtual_start.main()
        QMessageBox.information(
            window, "Completed", "Extraction of virtual section mileage completed! Saved in processed_data folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during virtual_start script execution: {e}")
    sys.stdout = sys.__stdout__


def run_virtual_end():
    sys.stdout = EmittingStream(output_area)
    try:
        virtual_end.main()
        QMessageBox.information(
            window, "Completed", "Extraction of virtual section mileage completed! Saved in processed_data folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during virtual_end script execution: {e}")
    sys.stdout = sys.__stdout__


def run_virtual_end_update():
    sys.stdout = EmittingStream(output_area)
    try:
        virtual_end_update.main()
        QMessageBox.information(
            window, "Completed", "Extraction of virtual section mileage completed! Saved in processed_data folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during virtual_end_update script execution: {e}")
    sys.stdout = sys.__stdout__


def run_combine_files():
    sys.stdout = EmittingStream(output_area)
    try:
        combine_files()
        QMessageBox.information(
            window, "Completed", "Extraction of virtual section mileage completed! Saved in processed_data folder!")
    except Exception as e:
        QMessageBox.critical(
            window, "Error", f"Error occurred during combine_files script execution: {e}")
    sys.stdout = sys.__stdout__


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('XLSX to CSV Converter')

layout = QVBoxLayout()

output_area = QTextEdit()
output_area.setReadOnly(True)
layout.addWidget(output_area)

xlsx_to_csv_button = QPushButton('Convert XLSX to CSV')
xlsx_to_csv_button.clicked.connect(run_xlsx_to_csv_script)
layout.addWidget(xlsx_to_csv_button)

csv_rename_button = QPushButton('Rename CSV Files')
csv_rename_button.clicked.connect(run_csv_rename_script)
layout.addWidget(csv_rename_button)

mks2chainage_button = QPushButton('Convert MIKE txt to chainage.csv')
mks2chainage_button.clicked.connect(run_mks2chainage_script)
layout.addWidget(mks2chainage_button)

chg_split_button = QPushButton('Split chainage.csv to sections')
chg_split_button.clicked.connect(run_chg_split)
layout.addWidget(chg_split_button)

chg_insert_button = QPushButton('insert')
chg_insert_button.clicked.connect(run_chg_insert)
layout.addWidget(chg_insert_button)

clean_csv_button = QPushButton('clean csv')
clean_csv_button.clicked.connect(run_clean_csv)
layout.addWidget(clean_csv_button)

mkcc_button = QPushButton('mkcc')
mkcc_button.clicked.connect(run_mkcc)
layout.addWidget(mkcc_button)


get_virtual_end_button = QPushButton('get virtual end')
get_virtual_end_button.clicked.connect(run_get_virtual_end)
layout.addWidget(get_virtual_end_button)

virtual_start_button = QPushButton('virtual start')
virtual_start_button.clicked.connect(run_virtual_start)
layout.addWidget(virtual_start_button)

virtual_end_button = QPushButton('virtual end')
virtual_end_button.clicked.connect(run_virtual_end)
layout.addWidget(virtual_end_button)

virtual_end_update_button = QPushButton('virtual end update')
virtual_end_update_button.clicked.connect(run_virtual_end_update)
layout.addWidget(virtual_end_update_button)

combine_files_button = QPushButton('combine files')
combine_files_button.clicked.connect(run_combine_files)
layout.addWidget(combine_files_button)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())

