import os
import sys
import pandas as pd
import shutil

# 确定基础目录
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def xlsx_to_csv(xlsx_file_path, csv_file_path):
    # 读取 Excel 文件
    df = pd.read_excel(xlsx_file_path)

    # 将其写入 CSV 文件
    df.to_csv(csv_file_path, index=False)


def copy_csv_files(src_dir, dst_dir, pattern):
    # 确保目标目录存在
    os.makedirs(dst_dir, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(src_dir):
        for filename in filenames:
            if filename.endswith(pattern):
                src_file = os.path.join(dirpath, filename)
                shutil.copy(src_file, dst_dir)
                print(f"Copied '{src_file}' to '{dst_dir}'")


def main():
    # 输入和输出目录都设置为 BASE_DIR 下的相应子目录
    resources_dir = os.path.join(BASE_DIR, 'resources')
    csv_files_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_files')
    csv_sections_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_sections')

    os.makedirs(csv_files_dir, exist_ok=True)  # 创建输出目录，如果不存在

    for dirpath, dirnames, filenames in os.walk(resources_dir):
        for filename in filenames:
            if filename.endswith('.xlsx'):
                folder_number = os.path.basename(dirpath).split('_')[0]
                xlsx_file_path = os.path.join(dirpath, filename)
                csv_file_name = folder_number + '_' + \
                    os.path.splitext(filename)[0] + '.csv'
                csv_file_path = os.path.join(csv_files_dir, csv_file_name)

                xlsx_to_csv(xlsx_file_path, csv_file_path)
                print(f"Converted '{xlsx_file_path}' to '{csv_file_path}'")

    # 复制特定的 CSV 文件到 csv_sections 目录
    copy_csv_files(csv_files_dir, csv_sections_dir, '断面测量数据表.csv')


if __name__ == '__main__':
    main()

