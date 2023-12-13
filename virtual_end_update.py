import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))# 设置输入和输出文件夹的路径
input_folder = os.path.join(BASE_DIR, 'processed_data', 'txt_virtual_start')
output_folder = os.path.join(BASE_DIR, 'processed_data', 'txt_virtual_end')
readcsvfile = os.path.join(BASE_DIR, 'processed_data', 'all_end_virtuals.csv')
# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 读取CSV文件，并创建一个映射（文件名到chainage）
df = pd.read_csv(readcsvfile, header=None,
                 names=['river', 'branch', 'chainage'])

chainage_map = {f"{row['river'].split('_')[0]}_{row['branch']}.txt": row['chainage']
                for index, row in df.iterrows()}

# 遍历每个文件
# paclage to def main


def main():
    for txt_filename, new_chainage in chainage_map.items():
        input_path = os.path.join(input_folder, txt_filename)
        output_path = os.path.join(output_folder, txt_filename)

        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                data = file.readlines()

            # 定位到倒数第二个分隔符后的第三行
            separator_indices = [index for index, line in enumerate(
                data) if line.strip() == '*******************************']
            if len(separator_indices) < 2:
                print(f"{txt_filename}: 分隔符数量不足，跳过该文件。")
                continue

            target_line_index = separator_indices[-2] + 3
            if target_line_index >= len(data):
                print(f"{txt_filename}: 目标行超出文件范围，跳过该文件。")
                continue

            # 替换该行内容
            data[target_line_index] = f"             {new_chainage}\n"

            # 将更新后的内容写回文件
            with open(output_path, 'w', encoding='utf-8') as file:
                file.writelines(data)

            print(f"{txt_filename}: 断面数据已更新。")

        except FileNotFoundError:
            print(f"{txt_filename}: 文件未找到。")

    print("所有操作已完成。")


if __name__ == '__main__':
    main()
