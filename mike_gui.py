import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
import os
import xlsx2csv_all  # 导入你的 xlsx 转换脚本
import csv_rn_cap  # 导入你的 csv 重命名脚本
import mks2chainage  # 导入你的 mks2chainage 脚本
import chg_split  # 导入你的 chg_split 脚本
import chg_insert  # 导入你的 chg_insert 脚本
import clean_csv  # 导入你的 clean_csv 脚本
import get_virtual_end  # 导入你的 get_virtual_end 脚本
import virtual_start

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class EmittingStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.append(message)

    def flush(self):
        pass


def run_xlsx_to_csv_script():
    xlsx2csv_all.BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    sys.stdout = EmittingStream(output_area)
    try:
        xlsx2csv_all.main()
        QMessageBox.information(window, "完成", "XLSX 到 CSV 转换完成！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"转换过程中出现错误：{e}")
    sys.stdout = sys.__stdout__


def run_csv_rename_script():
    sys.stdout = EmittingStream(output_area)  # 重定向输出到 QTextEdit
    try:
        csv_rn_cap.main()  # 直接运行 csv 重命名脚本的 main 函数
        QMessageBox.information(window, "完成", "CSV 文件重命名完成！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"重命名过程中出现错误：{e}")
    sys.stdout = sys.__stdout__  # 恢复标准输出


def run_mks2chainage_script():
    input_file_path = os.path.join(BASE_DIR, 'secss.txt')  # 定义输入文件路径
    sys.stdout = EmittingStream(output_area)
    try:
        mks2chainage.main(input_file_path)
        QMessageBox.information(
            window, "完成", "MIKE 断面文件转为里程csv文件完成,保存为chainage.csv！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"mks2chainage 脚本执行过程中出现错误：{e}")
    sys.stdout = sys.__stdout__


def run_chg_split():
    sys.stdout = EmittingStream(output_area)
    try:
        chg_split.main()
        QMessageBox.information(
            window, "完成", "根据chainage.csv文件分割断面完成！保存在chg_files文件夹中！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"chg_split 脚本执行过程中出现错误：{e}")
    sys.stdout = sys.__stdout__


def run_chg_insert():
    sys.stdout = EmittingStream(output_area)
    try:
        chg_insert.main()
        QMessageBox.information(
            window, "完成", "根据chainage files in chg_files 插入相关断面信息到对应文件 保存在 inserted_files 文件夹中！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"chg_split 脚本执行过程中出现错误：{e}")
    sys.stdout = sys.__stdout__


def run_clean_csv():
    sys.stdout = EmittingStream(output_area)
    try:
        clean_csv.main()
        QMessageBox.information(
            window, "完成", "根据chainage files in chg_files 插入相关断面信息到对应文件 保存在 inserted_files 文件夹中！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"run_clean_csv 脚本执行过程中出现错误：{e}")
    sys.stdout = sys.__stdout__

def run_get_virtual_end():
    sys.stdout = EmittingStream(output_area)
    try:
        get_virtual_end.main()
        QMessageBox.information(
            window, "完成", "虚拟断面里程提取完成！保存在 processed_data 文件夹中 ！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"run_get_virtual_end 脚本执行过程中出现错误：{e}")
    sys.stdout = sys.__stdout__

def run_virtual_start():
    sys.stdout = EmittingStream(output_area)
    try:
        virtual_start.main()
        QMessageBox.information(
            window, "完成", "虚拟断面里程提取完成！保存在 processed_data 文件夹中！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"run_get_virtual_end 脚本执行过程中出现错误：{e}")
    sys.stdout = sys.__stdout__

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('XLSX to CSV Converter')

layout = QVBoxLayout()

output_area = QTextEdit()
output_area.setReadOnly(True)
layout.addWidget(output_area)

xlsx_to_csv_button = QPushButton('Convert XLSX to CSV')
xlsx_to_csv_button.clicked.connect(run_xlsx_to_csv_script)
layout.addWidget(xlsx_to_csv_button)

csv_rename_button = QPushButton('Rename CSV Files')
csv_rename_button.clicked.connect(run_csv_rename_script)
layout.addWidget(csv_rename_button)

mks2chainage_button = QPushButton('Convert MIKE txt to chainage.csv')
mks2chainage_button.clicked.connect(run_mks2chainage_script)
layout.addWidget(mks2chainage_button)

chg_split_button = QPushButton('Split chainage.csv to sections')
chg_split_button.clicked.connect(run_chg_split)
layout.addWidget(chg_split_button)

chg_insert_button = QPushButton('insert')
chg_insert_button.clicked.connect(run_chg_insert)
layout.addWidget(chg_insert_button)

clean_csv_button = QPushButton('clean csv')
clean_csv_button.clicked.connect(run_clean_csv)
layout.addWidget(clean_csv_button)

get_virtual_end_button = QPushButton('get virtual end')
get_virtual_end_button.clicked.connect(run_get_virtual_end)
layout.addWidget(get_virtual_end_button)

virtual_start_button = QPushButton('virtual start')
virtual_start_button.clicked.connect(run_virtual_start)
layout.addWidget(virtual_start_button)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
