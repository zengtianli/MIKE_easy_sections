import pandas as pd
import os
import sys
# 设置输入和输出文件夹的路径
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

input_folder = os.path.join(BASE_DIR, 'processed_data', 'txt_virtual_start')
output_folder = os.path.join(BASE_DIR, 'processed_data', 'txt_virtual_end')
readcsvfile = os.path.join(BASE_DIR, 'processed_data', 'all_end_virtuals.csv')
# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.mkdir(output_folder)
# 读取CSV文件
df = pd.read_csv(readcsvfile, header=None,
                 names=['river', 'branch', 'chainage'])
# 遍历每一行，生成对应的.txt文件名


def main():
    """
    Process the .txt files in the input folder, extract the last complete section data,
    and append it to the corresponding output file in the output folder.
    """
    for index, row in df.iterrows():
        txt_filename = f"{row['river'].split('_')[0]}_{row['branch']}.txt"
        input_path = os.path.join(input_folder, txt_filename)
        print('input', input_path)
        output_path = os.path.join(output_folder, txt_filename)
        print('output', output_path)
        try:
            # Open and read the corresponding .txt file
            with open(input_path, 'r', encoding='utf-8') as file:
                data = file.read()
            # Split the section data
            sections = data.split('*******************************')
            last_section = sections[-2].strip()  # Get the last complete section data and remove leading/trailing whitespace
            # Copy and append the last section data to the end of the file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(data + '\n' + last_section +
                           '\n*******************************\n')
            print(f"{txt_filename}: Section data successfully appended.")
        except FileNotFoundError:
            print(f"{txt_filename}: File not found.")
    print("All operations completed.")


if __name__ == '__main__':
    main()
