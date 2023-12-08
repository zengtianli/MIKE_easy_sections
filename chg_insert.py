import csv
import sys
import os
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
input_file_path = os.path.join(BASE_DIR, 'secss.txt')  # 定义输入文件路径
output_csv_file = os.path.join(BASE_DIR, 'processed_data', 'chainage.csv')


def load_chainage_data(chainage_file):
    chainage_data = {}
    with open(chainage_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            if row[0] != 'null':
                # sections -> (branch, chainage_n, chainage_v)
                chainage_data[row[0]] = (row[1], row[2], row[3])
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
        elif row:
            output_data[branch].append(row)  # 添加其他数据行
    for branch, data in output_data.items():
        output_file = os.path.join(
            output_dir, f"{prefix}_{branch}.csv")
        with open(output_file, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


def main():
    if len(sys.argv) != 2:
        print("Usage: python chg_insert.py <section_file>")
        sys.exit(1)
    section_file = sys.argv[1]
    # 从输入文件名中构造chainage文件名
    chainage_file = os.path.join(
        '../00_chg_files/', os.path.basename(section_file).replace('.csv', '_chg.csv'))
    output_dir = '../processed_data/inserted_files'
    os.makedirs(output_dir, exist_ok=True)
    prefix = os.path.basename(section_file).split('_')[0]
    chainage_data = load_chainage_data(chainage_file)
    process_section_file(section_file, chainage_data, output_dir, prefix)
    print(f"Processed file: {section_file} stored in {output_dir}")


if __name__ == "__main__":
    main()
