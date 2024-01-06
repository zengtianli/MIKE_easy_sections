import glob
import csv
import sys
import os
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def clean_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        start_processing = False
        cleaned_data = []
        last_row_was_data = False

        for row in reader:
            if "断面名称" in row:
                start_processing = True
                cleaned_data.append(row)
                last_row_was_data = False
            elif start_processing:
                if last_row_was_data and "点号" in row[0]:
                    # 如果上一行是数据行且当前行是“点号”，则停止处理
                    break
                cleaned_data.append(row)
                last_row_was_data = row[0].isdigit()

    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(cleaned_data)


def main():
    input_dir = os.path.join(BASE_DIR, 'processed_data', 'inserted_files')
    output_dir = os.path.join(BASE_DIR,  'processed_data', 'inst_cle_files')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for input_file in glob.glob(os.path.join(input_dir, '*.csv')):
        print(f"🧼 Cleaning {input_file}...")
        output_file = os.path.join(output_dir, os.path.basename(input_file))
        clean_csv(input_file, output_file)
        print(f"Cleaned data saved to: {output_file}")


if __name__ == "__main__":
    main()
