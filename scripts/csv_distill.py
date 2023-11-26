import csv
import sys
import os

def process_csv(input_file, output_dir):
    with open(input_file, mode='r', encoding='utf-8') as infile:
        data = list(csv.reader(infile))

    processed_data = []
    chainage_count = 1
    for row in data:
        if row and row[0].isdigit():
            processed_data.append(row)
        elif "断面名称" in row:
            # 使用zfill确保chainage_count总是两位数
            chainage_label = f'chainage_{str(chainage_count).zfill(2)}'
            processed_data.append([chainage_label])
            chainage_count += 1

    # 构建输出文件的路径
    output_file = os.path.join(output_dir, os.path.basename(input_file))
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(processed_data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python csv_distill.py <input_file1> [<input_file2> ...]")
        sys.exit(1)

    # 创建输出目录
    output_dir = "../csv_distilled"
    os.makedirs(output_dir, exist_ok=True)

    # 处理每个文件
    for input_csv_file in sys.argv[1:]:
        process_csv(input_csv_file, output_dir)
        print(f"Processed file: {input_csv_file}")

