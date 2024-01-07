# script_mappings.py is a dictionary of script names and their corresponding functions
from scripts import xlsx2csv_all, csv_rn_cap, mks2chainage, chg_split, chg_insert, clean_csv, get_virtual_end, virtual_start, mkcc, virtual_end, virtual_end_update
import sys
import os
import glob

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
