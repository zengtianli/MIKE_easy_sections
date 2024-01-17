# mks2chainage.py
from PyQt6.QtWidgets import QMessageBox
import csv
import subprocess
import os
import sys
import re
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
input_file_path = os.path.join(BASE_DIR, 'secss.txt')  # 定义输入文件路径
output_csv_file = os.path.join(BASE_DIR, 'processed_data', 'chainage.csv')


def auto_virtual_add(data):
    """
    Add 'virtual' to the start and end of chainages in the given data.

    Args:
        data (dict): A dictionary containing branch names as keys and chainages as values.

    Returns:
        dict: The updated data dictionary with 'virtual' added to the start and end of chainages.
    """
    for branch_name, chainages in data.items():
        if len(chainages) > 1:  # Check if there are at least two chainages
            # Add 'virtual' to the start
            chainages[0] = (*chainages[0], 'virtual')
            # Add 'virtual' to the end
            chainages[-1] = (*chainages[-1], 'virtual')
        elif len(chainages) == 1:  # If there's only one chainage
            # Add 'virtual' to the only chainage
            chainages[0] = (*chainages[0], 'virtual')
    return data


def process_file(file_path, csv_file_path, use_auto_virtual_add=False):
    """
    Process the input file and generate a CSV file with chainage data.

    Args:
        file_path (str): The path to the input file.
        csv_file_path (str): The path to the output CSV file.
        use_auto_virtual_add (bool, optional): Flag indicating whether to use auto virtual add. Defaults to False.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {}
    current_branch = None
    chainage_count = 0
    branch_numbers = {}
    current_number = 1
    for i, line in enumerate(lines):
        if i + 3 < len(lines) and "COORDINATES" in lines[i + 3]:
            new_branch_full = lines[i].strip()
            new_branch_base = re.sub(r'\d+', '', new_branch_full)
            if new_branch_base not in branch_numbers:
                branch_numbers[new_branch_base] = f"{current_number:02d}_{new_branch_base}"
                current_number += 1
            if new_branch_full != current_branch:
                current_branch = new_branch_full
                chainage_count = 0
                data[current_branch] = []
            chainage_number = lines[i + 2].strip()
            data[current_branch].append((chainage_count, chainage_number))
            chainage_count += 1
    if use_auto_virtual_add:
        data = auto_virtual_add(data)
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['river', 'sections', 'branch',
                           'chainage_n', 'chainage_v'])
        for branch_name, chainages in data.items():
            branch_base = re.sub(r'\d+', '', branch_name)
            river_name = branch_numbers.get(branch_base, "")
            for chainage in chainages:
                chainage_count, chainage_number, *sections = chainage
                sections_value = sections[0] if sections else ""
                formatted_chainage = f"chainage_{chainage_count:02d}"
                csvwriter.writerow(
                    [river_name, sections_value, branch_name, formatted_chainage, chainage_number])


def open_in_excel(csv_file_path):
    """
    Opens the given CSV file in Excel.

    Parameters:
    csv_file_path (str): The path to the CSV file.

    Returns:
    None
    """
    # Open the CSV file in Excel
    if sys.platform == "win32":
        os.startfile(csv_file_path)  # For Windows
    elif sys.platform == "darwin":
        subprocess.call(["open", csv_file_path])  # For macOS
    else:
        subprocess.call(["xdg-open", csv_file_path])  # For Linux


def main(input_file=input_file_path):
    """
    Main function to process the input file and generate output.

    Args:
        input_file (str): Path to the input file.

    Returns:
        None
    """
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Process File")
    msgBox.setText("Do you want to automatically add 'virtual' to chainages?")
    msgBox.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    result = msgBox.exec()

    use_auto_virtual_add = result == QMessageBox.StandardButton.Yes

    process_file(input_file, output_csv_file, use_auto_virtual_add)
    open_in_excel(output_csv_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python mks2chainage.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
