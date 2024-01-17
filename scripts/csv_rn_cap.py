# csv_rn_cap.py
import os
from pypinyin import lazy_pinyin, Style
import sys

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def get_pinyin_initials(text):
    """
    Get the initials of the pinyin representation of the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The initials of the pinyin representation of the text.
    """
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
    """
    Renames files in the specified directory by removing the substring '断面测量数据表' from the filename.

    Args:
        directory (str): The directory path where the files are located.

    Returns:
        None
    """
    for filename in os.listdir(directory):
        if filename.endswith("断面测量数据表.csv"):
            new_filename = filename.replace("断面测量数据表", "").strip()
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)
            os.rename(old_filepath, new_filepath)
            print(f"Renamed '{filename}' to '{new_filename}'")


def rename_files_to_pinyin(directory):
    """
    Renames all CSV files in the specified directory to include the pinyin initials of the second part of the filename.

    Args:
        directory (str): The directory path where the CSV files are located.

    Returns:
        None
    """
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
    """
    This function is the entry point of the script.
    It renames files in the csv_sections directory and then renames them to pinyin.
    """
    csv_sections_dir = os.path.join(BASE_DIR, 'processed_data', 'csv_sections')
    rename_files(csv_sections_dir)
    rename_files_to_pinyin(csv_sections_dir)


if __name__ == "__main__":
    main()
