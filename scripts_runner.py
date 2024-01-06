from PyQt6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit, QHBoxLayout, QMenuBar, QMainWindow, QDialog, QLabel, QLineEdit, QKeySequenceEdit)

from scripts import xlsx2csv_all, csv_rn_cap, mks2chainage, chg_split, chg_insert, clean_csv, get_virtual_end, virtual_start, mkcc, virtual_end, virtual_end_update
import os
import sys
class EmittingStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.append(message)

    def flush(self):
        pass


def execute_script(script_func, success_message, error_message, output_area, window, *args):
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
# def run_xlsx_to_csv_script(output_area): xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0])); execute_script( xlsx2csv_all.main, "XLSX to <u>CSV</u> conversion completed!", "Error occurred during conversion")
def run_xlsx_to_csv_script(output_area, window):
    xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    execute_script(xlsx2csv_all.main, "XLSX to <u>CSV</u> conversion completed!", "Error occurred during conversion", output_area, window)

def run_csv_rename_script(): execute_script( csv_rn_cap.main, "CSV file renaming completed!", "Error occurred during renaming")
def run_mks2chainage_script(): input_file_path = os.path.join(BASE_DIR, 'secss.txt'); execute_script( mks2chainage.main, "according to MIKE section file(txt) generate a mileage csv completed, saved as <u>chainage.csv</u> (need modify manually)!", "Error occurred during mks2chainage script execution", input_file_path)
def run_chg_split(): execute_script( chg_split.main, "Section split according to chainage.csv file completed! Saved in <u>chg_files</u> folder!", "Error occurred during chg_split script execution")
def run_chg_insert(): execute_script( chg_insert.main, "Insertion of related section information from chg_files into corresponding files ! Saved in <u>inserted_files</u> folder!", "Error occurred during chg_insert script execution")
def run_clean_csv(): execute_script( clean_csv.main, "clean csv data completed! Saved in <u>cleaned_files</u> folder!", "Error occurred during clean_csv script execution")
def run_mkcc(): execute_script( mkcc.main, "according to csv files generate MIKE section file(txt) completed! Saved in <u>txt_files</u> folder!", "Error occurred during mkcc script execution")
def run_get_virtual_end(): execute_script( get_virtual_end.main, "Extract virtual section from chg_files and combine them into <u>all_virtual_end.csv </u>", "Error occurred during get_virtual_end script execution")
def run_virtual_start(): execute_script( virtual_start.main, "add start virtual section to txt files, save in  <u>txt_virtual_start</u> folder! ", "Error occurred during virtual_start script execution")
def run_virtual_end(): execute_script( virtual_end.main, "add end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!", "Error occurred during virtual_end script execution")
def run_virtual_end_update(): execute_script( virtual_end_update.main, "update end virtual section to txt files, save in  <u>txt_virtual_end</u> folder!", "Error occurred during virtual_end_update script execution")
def run_combine_files(): execute_script( combine_files, "Combine all txt files into <u>combined.txt</u> file!", "Error occurred during combine_files script execution")
# def run_conversion_module(): run_xlsx_to_csv_script(); run_csv_rename_script()
def run_conversion_module(output_area, window): run_xlsx_to_csv_script(output_area, window); run_csv_rename_script()
def run_processing_module(): run_mks2chainage_script(); run_chg_split(); run_chg_insert(); run_clean_csv(); run_mkcc()
def run_virtual_section_module(): run_get_virtual_end(); run_virtual_start(); run_virtual_end(); run_virtual_end_update(); run_combine_files()

