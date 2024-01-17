# virtual_start.py
import os
import glob
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
input_dir = os.path.join(BASE_DIR, 'processed_data', 'txt_files')
output_dir = os.path.join(BASE_DIR, 'processed_data', 'txt_virtual_start')

def insert_virtual_section(input_file, output_dir):
    """
    Inserts a virtual section at the beginning of the file.

    Args:
        input_file (str): The path to the input file.
        output_dir (str): The directory where the modified file will be saved.

    Returns:
        None
    """
    # 读取原始文件内容
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 寻找第一个断面的结束位置
    first_section_end = None
    for i, line in enumerate(lines):
        if line.strip() == "*******************************":
            first_section_end = i
            break
    if first_section_end is None:
        print("未找到第一个断面的结束标记。")
        return
    # 复制第一个断面并修改chainage值
    virtual_section = lines[:first_section_end + 1]
    virtual_section[2] = "             0.000\n"  # 修改chainage值
    # 确保在虚拟断面和原始断面之间有换行分隔
    if virtual_section[-1].strip() == "*******************************":
        virtual_section.append("\n")
    # 插入虚拟断面到文件开始处
    modified_content = virtual_section + lines
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 保存修改后的文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(modified_content)
    print(f"文件已处理并保存为：{output_file}")


def process_directory(input_dir, output_dir):
    """
    Process all the text files in the input directory and insert virtual sections into the output directory.

    Args:
        input_dir (str): The path to the input directory.
        output_dir (str): The path to the output directory.

    Returns:
        None
    """
    # 获取目录下所有文件
    for input_file in glob.glob(os.path.join(input_dir, '*.txt')):
        insert_virtual_section(input_file, output_dir)


def main():
    """
    This is the main function that processes the input directory and creates the output directory if it doesn't exist.
    """
    # input_dir = "../processed_data/txt_files"
    # output_dir = "../processed_data/txt_virtual_start"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    process_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
