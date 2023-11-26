import os
from pypinyin import lazy_pinyin


def get_pinyin_initials(text):
    return ''.join([word[0].upper() for word in lazy_pinyin(text) if word.isalpha()])


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
                new_filename = parts[0] + '_' + pinyin_initials + '.csv'
                old_filepath = os.path.join(directory, filename)
                new_filepath = os.path.join(directory, new_filename)
                os.rename(old_filepath, new_filepath)
                print(f"Renamed '{filename}' to '{new_filename}'")


if __name__ == "__main__":
    directory = "../csv_sections"  # 假设当前目录包含上述文件
    rename_files(directory)
    rename_files_to_pinyin(directory)
