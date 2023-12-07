import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTextEdit
from PyQt5.QtGui import QIcon
import os
import xlsx2csv_all  # 导入你的 xlsx 转换脚本
import csv_rn_cap  # 导入你的 csv 重命名脚本
import mks2chainage  # 导入你的 mks2chainage 脚本

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
    # debug input_file_path
    # print(input_file_path)
    try:
        mks2chainage.main(input_file_path)
        QMessageBox.information(
            window, "完成", "MIKE 断面文件转为里程csv文件完成,保存为chainage.csv！")
    except Exception as e:
        QMessageBox.critical(window, "错误", f"mks2chainage 脚本执行过程中出现错误：{e}")
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

mks2chainage_button = QPushButton('Run mks2chainage Script')
mks2chainage_button.clicked.connect(run_mks2chainage_script)
layout.addWidget(mks2chainage_button)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())
