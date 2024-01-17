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
    """
    Executes a script based on the given script name.

    Args:
        script_name (str): The name of the script to execute.
        window: The window object to display message boxes.
        output_area: The output area to redirect stdout.
        *args: Optional arguments to pass to the script function.

    Raises:
        Exception: If an error occurs during script execution.

    Returns:
        None
    """
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
    """
    Converts an Excel file to CSV format using the 'xlsxToCsv' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("xlsxToCsv", window, output_area)


def R_rename_csv(window, output_area):
    """
    Renames a CSV file using the 'renameCsv' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("renameCsv", window, output_area)


def R_mks2chain(window, output_area):
    """
    Converts MKS file to chain CSV format.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("mkChainCsv", window, output_area)


def R_split_chg(window, output_area):
    """
    Executes the 'splitChg' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("splitChg", window, output_area)


def R_insert_chg(window, output_area):
    """
    Executes the 'insertChg' script.

    Args:
        window: The window object.
        output_area: The output area object.
    """
    execute_script("insertChg", window, output_area)


def R_clean_csv(window, output_area):
    """
    Executes the 'cleanCsv' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("cleanCsv", window, output_area)


def R_mkcc(window, output_area):
    """
    Executes the 'mkMikeTxt' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("mkMikeTxt", window, output_area)


def R_get_virt_end(window, output_area):
    """
    Executes the 'getVirtEnd' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("getVirtEnd", window, output_area)


def R_virt_start(window, output_area):
    """
    Executes the 'virtStart' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("virtStart", window, output_area)


def R_virt_end(window, output_area):
    """
    Executes the 'virtEnd' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("virtEnd", window, output_area)


def R_upd_virt_end(window, output_area):
    """
    Executes the 'updateVirtEnd' script.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    execute_script("updateVirtEnd", window, output_area)


def R_combine_txt(window, output_area):
    """
    Executes the 'combineTxt' script.

    Args:
        window: The window object.
        output_area: The output area object.
    """
    execute_script("combineTxt", window, output_area)


def R_conv_module(window, output_area):
    """
    Converts XLSX files to CSV format and renames the CSV files.

    Args:
        window: The window object.
        output_area: The output area object.

    Returns:
        None
    """
    try:
        R_xlsx2csv(window, output_area)
        R_rename_csv(window, output_area)
    except Exception as e:
        print(f"Error in conversion module: {e}")
        return  # Stop execution if an error occurs


def R_proc_module(window, output_area):
    """
    Executes a series of R functions to process data.

    Args:
        window: The window object representing the application window.
        output_area: The output area object where the results will be displayed.

    Returns:
        None
    """
    try:
        # R_mks2chain(window, output_area)  # Uncomment if needed
        R_split_chg(window, output_area)
        R_insert_chg(window, output_area)
        R_clean_csv(window, output_area)
        R_mkcc(window, output_area)
    except Exception as e:
        print(f"Error in processing module: {e}")
        return  # Stop execution if an error occurs


def R_virt_sect_mod(window, output_area):
    """
    Executes a series of R functions to modify virtual sections.

    Parameters:
    - window: The window object.
    - output_area: The output area object.

    Returns:
    None
    """
    try:
        R_get_virt_end(window, output_area)
        R_virt_start(window, output_area)
        R_virt_end(window, output_area)
        R_upd_virt_end(window, output_area)
        R_combine_txt(window, output_area)
    except Exception as e:
        print(f"Error in virtual section module: {e}")
        return  # Stop execution if an error occurs

