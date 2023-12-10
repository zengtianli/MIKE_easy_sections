import csv
import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

input_dir = os.path.join(BASE_DIR, 'processed_data', 'chg_files')
# output_dir = os.path.join(BASE_DIR,  'processed_data', 'all_end_virtuals.csv')
output_file = os.path.join(BASE_DIR,'processed_data' ,'all_end_virtuals.csv')  # Define output_file variable

def extract_virtual_chainage(input_file):
    virtual_chainage = []
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # 检查是否为虚拟断面且chainage_v不为0
            print(row)
            if row[1] == 'virtual' and row[4] != '0.000':
                print(f"Found virtual end at {row[3]}")
                virtual_chainage.append(
                    [os.path.basename(input_file).replace('_chg.csv', ''), row[1], row[3]])
    return virtual_chainage


def main():
    all_virtual_chainage = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            virtual_chainage = extract_virtual_chainage(
                os.path.join(input_dir, filename))
            all_virtual_chainage.extend(virtual_chainage)

    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_virtual_chainage)

    print(f"Virtual chainage extracted to {output_file}")


if __name__ == "__main__":
    main()
