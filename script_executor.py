# script_executor.py
import sys
from PyQt6.QtWidgets import QMessageBox
from script_mappings import script_mappings


class EmittingStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.append(message)

    def flush(self):
        pass


def execute_script(script_name, window, output_area, *args):
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


def R_xlsx2csv(window, output_area):
    execute_script("xlsx_to_csv", window, output_area)


def R_rename_csv(window, output_area):
    execute_script("csv_rename", window, output_area)


def R_mks2chain(window, output_area):
    execute_script("mks2chainage", window, output_area)


def R_split_chg(window, output_area):
    execute_script("chg_split", window, output_area)


def R_insert_chg(window, output_area):
    execute_script("chg_insert", window, output_area)


def R_clean_csv(window, output_area):
    execute_script("clean_csv", window, output_area)


def R_mkcc(window, output_area):
    execute_script("mkcc", window, output_area)


def R_get_virt_end(window, output_area):
    execute_script("get_virtual_end", window, output_area)


def R_virt_start(window, output_area):
    execute_script("virtual_start", window, output_area)


def R_virt_end(window, output_area):
    execute_script("virtual_end", window, output_area)


def R_upd_virt_end(window, output_area):
    execute_script("virtual_end_update", window, output_area)


def R_combine_txt(window, output_area):
    execute_script("combine_files", window, output_area)


def R_conv_module(window, output_area):
    R_xlsx2csv(window, output_area)
    R_rename_csv(window, output_area)


def R_proc_module(window, output_area):
    R_mks2chain(window, output_area)
    R_split_chg(window, output_area)
    R_insert_chg(window, output_area)
    R_clean_csv(window, output_area)
    R_mkcc(window, output_area)


def R_virt_sect_mod(window, output_area):
    R_get_virt_end(window, output_area)
    R_virt_start(window, output_area)
    R_virt_end(window, output_area)
    R_upd_virt_end(window, output_area)
    R_combine_txt(window, output_area)
