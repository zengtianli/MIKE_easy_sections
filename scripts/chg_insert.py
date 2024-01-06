import csv
import sys
import os
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def load_chainage_data(chainage_file):
    """
    Load chainage data from a file and return a dictionary.

    Args:
        chainage_file (str): The path to the chainage file.

    Returns:
        dict: A dictionary containing the chainage data, where the keys are the chainage IDs
              and the values are tuples containing the corresponding data.

    """
    chainage_data = {}
    with open(chainage_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[1] != 'virtual':
                chainage_data[row[1]] = (row[2], row[3], row[4])
    return chainage_data


def process_section_file(section_file, chainage_data, output_dir, prefix):
    with open(section_file, mode='r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
    output_data = {}
    for branch in set(val[0] for val in chainage_data.values()):
        output_data[branch] = []
    for row in reader:
        if row and "断面名称" in row[0]:
            current_section = row[1]
            if current_section in chainage_data:
                branch, chainage_n, chainage_v = chainage_data[current_section]
                output_data[branch].append(row)  # 添加断面名称行
                output_data[branch].append(
                    [f"{current_section},{branch},{chainage_n},{chainage_v}"])  # 添加chainage行
        elif row: output_data[branch].append(row)  # 添加其他数据行
    for branch, data in output_data.items():
        output_file = os.path.join(
            output_dir, f"{prefix}_{branch}.csv")
        with open(output_file, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


def main():
    input_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_sections')
    chainage_files_dir = os.path.join(BASE_DIR, 'processed_data', 'chg_files')
    output_dir = os.path.join(BASE_DIR,  'processed_data', 'inserted_files')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for section_file in os.listdir(input_dir):
        if section_file.endswith('.csv'):
            full_section_file_path = os.path.join(input_dir, section_file)
            chainage_file = os.path.join(
                chainage_files_dir, os.path.basename(section_file).replace('.csv', '_chg.csv'))
            prefix = os.path.basename(section_file).split('_')[0]
            chainage_data = load_chainage_data(chainage_file)
            process_section_file(full_section_file_path,
                                 chainage_data, output_dir, prefix)
            print(
                f"Processed file: {full_section_file_path} stored in {output_dir}")


if __name__ == "__main__":
    main()

