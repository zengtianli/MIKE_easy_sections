# mks2chainage_qtable.py
# mks2chainage.py
import csv
import subprocess
import os
import sys
import re
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
input_file_path = os.path.join(BASE_DIR, 'secss.txt')  # 定义输入文件路径
output_csv_file = os.path.join(BASE_DIR, 'processed_data', 'chainage.csv')

def process_file(file_path, csv_file_path):
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
            new_branch_base = re.sub(r'\d+', '', new_branch_full)  # Remove numbers
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
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['river', 'sections', 'branch', 'chainage_n', 'chainage_v'])
        for branch_name, chainages in data.items():
            branch_base = re.sub(r'\d+', '', branch_name)
            river_name = branch_numbers.get(branch_base, "")
            for chainage in chainages:
                formatted_chainage = f"chainage_{chainage[0]:02d}"
                csvwriter.writerow([river_name, '', branch_name, formatted_chainage, chainage[1]])

# def open_in_excel(csv_file_path):
#     # Open the CSV file in Excel
#     if sys.platform == "win32":
#         os.startfile(csv_file_path)  # For Windows
#     elif sys.platform == "darwin":
#         subprocess.call(["open", csv_file_path])  # For macOS
#     else:
#         subprocess.call(["xdg-open", csv_file_path])  # For Linux
# def main(input_file_path=input_file_path):
#     # use this method :csv_files_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_files')
#     process_file(input_file_path, output_csv_file)
#     open_in_excel(output_csv_file)

def display_in_table(csv_file_path):
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('CSV Viewer')
    layout = QVBoxLayout()

    table_widget = QTableWidget()
    layout.addWidget(table_widget)
    window.setLayout(layout)

    with open(csv_file_path, 'r', newline='') as file:
        csv_data = list(csv.reader(file))
        table_widget.setRowCount(len(csv_data))
        table_widget.setColumnCount(len(csv_data[0]))
        for row_index, row_data in enumerate(csv_data):
            for column_index, cell_data in enumerate(row_data):
                table_widget.setItem(row_index, column_index, QTableWidgetItem(cell_data))

    window.show()
    sys.exit(app.exec())

def main(input_file_path=input_file_path):
    process_file(input_file_path, output_csv_file)
    display_in_table(output_csv_file)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python mks2chainage.py <input_file>")
        sys.exit(1)
    main(sys.argv[1])
