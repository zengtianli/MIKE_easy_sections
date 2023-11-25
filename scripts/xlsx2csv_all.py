import pandas as pd
import os


def xlsx_to_csv(xlsx_file_path, csv_file_path):
    # Read the Excel file
    df = pd.read_excel(xlsx_file_path)

    # Write to a CSV file
    df.to_csv(csv_file_path, index=False)


# 设置输出目录为scripts同级的csv_files文件夹
output_dir = os.path.join(os.path.dirname(__file__), '../csv_files')
os.makedirs(output_dir, exist_ok=True)  # 创建目录，如果不存在

# 遍历上级目录中的所有文件
for dirpath, dirnames, filenames in os.walk('..'):
    for filename in filenames:
        if filename.endswith('.xlsx'):
            # 获取所在文件夹的编号（如 01, 02等）
            folder_number = os.path.basename(dirpath).split('_')[0]

            # 构建文件路径
            xlsx_file_path = os.path.join(dirpath, filename)
            csv_file_name = folder_number + '_' + \
                os.path.splitext(filename)[0] + '.csv'
            csv_file_path = os.path.join(output_dir, csv_file_name)

            # 转换文件
            xlsx_to_csv(xlsx_file_path, csv_file_path)
            print(f"Converted '{xlsx_file_path}' to '{csv_file_path}'")

