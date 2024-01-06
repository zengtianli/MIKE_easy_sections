import os
from pypinyin import lazy_pinyin, Style
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def get_pinyin_initials(text):
    initials = []
    for char in text:
        # 对每个字符单独处理多音字
        if char == '长':
            initials.append('C')
        elif char == '重':
            initials.append('C')
        else:
            pinyin = lazy_pinyin(char, style=Style.NORMAL)
            if pinyin and pinyin[0].isalpha():
                initials.append(pinyin[0][0].upper())
    return ''.join(initials)


def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith("断面测量数据表.csv"):
            new_filename = filename.replace("断面测量数据表", "").strip()
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)
            os.rename(old_filepath, new_filepath)
            print(f"Renamed '{filename}' to '{new_filename}'")


def rename_files_to_pinyin(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            parts = filename.split('_')
            if len(parts) > 1:
                pinyin_initials = get_pinyin_initials(parts[1])
                new_filename = parts[0] + '_' + pinyin_initials[0:-3] + '.csv'
                old_filepath = os.path.join(directory, filename)
                new_filepath = os.path.join(directory, new_filename)
                os.rename(old_filepath, new_filepath)
                print(f"Renamed '{filename}' to '{new_filename}'")


def main():
    csv_sections_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_sections')
    rename_files(csv_sections_dir)
    rename_files_to_pinyin(csv_sections_dir)


if __name__ == "__main__":
    main()
