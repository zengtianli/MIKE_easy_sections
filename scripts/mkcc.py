# mkcc.py
import csv
import sys
import os

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
txt_folder = os.path.join(BASE_DIR, 'processed_data', 'txt_files')
csv_folder = os.path.join(BASE_DIR, 'processed_data', 'inst_cle_files')


def parse_csv_line(row):
    """解析CSV文件中的一行，返回坐标值和标签

    Args:
        row (list): 一行CSV数据

    Returns:
        tuple: 包含坐标值的元组，格式为 (x, y)
    """
    # 定义缺省值为0.0
    default_value = 0.0
    x = row[5].strip() if row[5].strip() else default_value
    y = row[4].strip() if row[4].strip() else default_value
    return float(x), float(y)  # 转换为浮点数以便于比较


def assign_tags(coordinates):
    """为坐标点分配标签

    Args:
        coordinates (list): A list of coordinate tuples (x, y).

    Returns:
        list: A list of tuples containing the coordinates and their assigned tags.

    """
    if not coordinates:
        return []
    min_x = min(coordinates, key=lambda c: c[0])
    max_x = max(coordinates, key=lambda c: c[0])
    min_y = min(coordinates, key=lambda c: c[1])
    tagged_coords = []
    for x, y in coordinates:
        if (x, y) == min_x:
            tag = "<#1>"  # 最左岸
        elif (x, y) == max_x:
            tag = "<#4>"  # 最右岸
        elif (x, y) == min_y:
            tag = "<#2>"  # 最低点
        else:
            tag = "<#0>"  # 其他点
        tagged_coords.append((x, y, tag))
    return tagged_coords


def format_txt_section(branch, chainage, coordinates):
    """将提取的数据格式化为TXT文件所需的格式

    Args:
        branch (str): The branch name.
        chainage (float): The chainage value.
        coordinates (list): A list of coordinates.

    Returns:
        str: The formatted section in TXT file format.
    """
    formatted_lines = [
        branch,
        branch,
        f"             {chainage}",
        "COORDINATES",
        "    0",
        # 其他静态文本内容
        "FLOW DIRECTION",
        "    0",
        "PROTECT DATA",
        "    0",
        "DATUM",
        "      0.00",
        "RADIUS TYPE",
        "    0",
        "DIVIDE X-Section",
        "0",
        "SECTION ID",
        " ",
        "INTERPOLATED",
        "    0",
        "ANGLE",
        "    0.00   0",
        "RESISTANCE NUMBERS",
        "   1  0     1.000     1.000     1.000    1.000    1.000",
        "PROFILE        3",
    ]
    for coord in coordinates:
        formatted_lines.append(
            f"     {coord[0]}     {coord[1]}     1.000     {coord[2]}     0     0.000     0")
    formatted_lines.append("LEVEL PARAMS")
    formatted_lines.append("   0  0    0.000  0    0.000  50")
    formatted_lines.append("*******************************")
    return '\n'.join(formatted_lines)


def convert_csv_to_txt(csv_path, txt_path):
    """
    Convert a CSV file to a TXT file containing formatted section data.

    Args:
        csv_path (str): The path to the input CSV file.
        txt_path (str): The path to the output TXT file.

    Returns:
        None
    """
    branch = os.path.basename(csv_path).split(
        '_')[1].split('.')[0]  # 提取文件名中的分支名称
    with open(csv_path, 'r') as csv_file, open(txt_path, 'w') as txt_file:
        reader = csv.reader(csv_file)
        coordinates = []
        chainage = ""
        for row in reader:
            if "断面名称" in row[0]:
                if coordinates:
                    tagged_coordinates = assign_tags(coordinates)
                    txt_file.write(format_txt_section(
                        branch, chainage, tagged_coordinates) + '\n')
                    coordinates = []
            elif "chainage" in row[0]:
                chainage = row[0].split(',')[-1].strip()  # 提取chainage值
            elif row[0].isdigit():  # 检查是否为数据行
                coordinates.append(parse_csv_line(row))
        if coordinates:
            tagged_coordinates = assign_tags(coordinates)
            txt_file.write(format_txt_section(
                branch, chainage, tagged_coordinates))


import glob

def main():
    """
    Converts CSV files to TXT files.

    This function searches for CSV files in a specified folder, converts each CSV file to a TXT file,
    and saves the converted files in a separate folder. The function also prints the conversion status
    for each file.

    Args:
        None

    Returns:
        None
    """
    csv_files = glob.glob(csv_folder + '/*.csv')
    for csv_file in csv_files:
        txt_file = csv_file.replace('.csv', '.txt')
        if not os.path.exists(txt_folder):
            os.makedirs(txt_folder)
        txt_file = os.path.join(txt_folder, os.path.basename(txt_file))
        convert_csv_to_txt(csv_file, txt_file)
        print(f"Converted {csv_file} to {txt_file}")

if __name__ == "__main__":
    main()
