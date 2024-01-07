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
    "xlsxToCsv": {
        "func": xlsx2csv_all.main,
        "success_msg": "XLSX to <u>CSV</u> conversion completed!",
        "error_msg": "Error occurred during conversion"
    },
    "renameCsv": {
        "func": csv_rn_cap.main,
        "success_msg": "CSV file renaming completed!",
        "error_msg": "Error occurred during renaming"
    },
    "mkChainCsv": {
        "func": mks2chainage.main,
        "success_msg": "Mileage CSV generation completed, saved as <u>chainage.csv</u>!",
        "error_msg": "Error occurred during mileage CSV generation"
    },
    "splitChg": {
        "func": chg_split.main,
        "success_msg": "Section split by chainage completed! Saved in <u>chg_files</u> folder!",
        "error_msg": "Error occurred during section split"
    },
    "insertChg": {
        "func": chg_insert.main,
        "success_msg": "Section info insertion from chg_files completed! Saved in <u>inserted_files</u> folder!",
        "error_msg": "Error occurred during section info insertion"
    },
    "cleanCsv": {
        "func": clean_csv.main,
        "success_msg": "CSV data cleaned! Saved in <u>cleaned_files</u> folder!",
        "error_msg": "Error occurred during CSV cleaning"
    },
    "mkMikeTxt": {
        "func": mkcc.main,
        "success_msg": "MIKE section file generation from CSV completed! Saved in <u>txt_files</u> folder!",
        "error_msg": "Error occurred during MIKE section file generation"
    },
    "getVirtEnd": {
        "func": get_virtual_end.main,
        "success_msg": "Virtual section extraction and combination completed!",
        "error_msg": "Error occurred during virtual section processing"
    },
    "virtStart": {
        "func": virtual_start.main,
        "success_msg": "Start virtual section added to txt files! Saved in <u>txt_virtual_start</u> folder!",
        "error_msg": "Error occurred during start virtual section addition"
    },
    "virtEnd": {
        "func": virtual_end.main,
        "success_msg": "End virtual section added to txt files! Saved in <u>txt_virtual_end</u> folder!",
        "error_msg": "Error occurred during end virtual section addition"
    },
    "updateVirtEnd": {
        "func": virtual_end_update.main,
        "success_msg": "End virtual section updated in txt files! Saved in <u>txt_virtual_end</u> folder!",
        "error_msg": "Error occurred during end virtual section update"
    },
    "combineTxt": {
        "func": combine_files,
        "success_msg": "All txt files combined into <u>combined.txt</u>!",
        "error_msg": "Error occurred during txt file combination"
    }
}
