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
    for index, row in df.iterrows():
        txt_filename = f"{row['river'].split('_')[0]}_{row['branch']}.txt"
        input_path = os.path.join(input_folder, txt_filename)
        print('input',input_path)
        output_path = os.path.join(output_folder, txt_filename)
        print('output',output_path)
        try:
            # 打开并读取对应的.txt文件
            with open(input_path, 'r', encoding='utf-8') as file:
                data = file.read()
            # 分割断面数据
            sections = data.split('*******************************')
            last_section = sections[-2].strip()  # 获取最后一个完整的断面数据并移除首尾空白字符
            # 将最后一个断面数据复制并追加到文件末尾
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(data + '\n' + last_section +
                           '\n*******************************\n')
            print(f"{txt_filename}: 断面数据已成功追加。")
        except FileNotFoundError:
            print(f"{txt_filename}: 文件未找到。")
    print("所有操作已完成。")


if __name__ == '__main__':
    main()
