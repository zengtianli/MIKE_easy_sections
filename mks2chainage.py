import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

input_file_path = os.path.join(BASE_DIR, 'secss.txt')  # 定义输入文件路径
output_csv_file = os.path.join(BASE_DIR, 'processed_data', 'chainage.csv')


def process_file(file_path, csv_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_branch = None
    chainage_count = 0

    for i, line in enumerate(lines):
        if i + 3 < len(lines) and "COORDINATES" in lines[i + 3]:
            new_branch = lines[i].strip()
            if new_branch != current_branch:
                current_branch = new_branch
                chainage_count = 0
                data[current_branch] = []

            chainage_number = lines[i + 2].strip()
            data[current_branch].append((chainage_count, chainage_number))
            chainage_count += 1

    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['river', 'sections', 'branch',
                           'chainage_n', 'chainage_v'])  # Header row

        for branch_name, chainages in data.items():
            for chainage in chainages:
                formatted_chainage = f"chainage_{chainage[0]:02d}"
                csvwriter.writerow(
                    [branch_name, formatted_chainage, chainage[1]])


def main(input_file_path=input_file_path):
    # use this method :csv_files_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_files')
    process_file(input_file_path, output_csv_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python mks2chainage.py <input_file>")
        sys.exit(1)

    main(sys.argv[1])

