import csv


def convert_csv_to_txt(csv_file, txt_file):
    # 读取 CSV 文件
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        lines = list(reader)

    # 提取 CSV 文件中的关键信息
    section_name = lines[0][1]
    chainage = lines[0][5]
    points = lines[2:]
    # 创建并写入 TXT 文件
    with open(txt_file, 'w', encoding='utf-8') as file:
        file.write(f"{section_name}\n")
        file.write(f"{section_name}\n")
        file.write(f"              {chainage}\n")
        file.write("COORDINATES\n    0\n")
        file.write("FLOW DIRECTION\n    0      \n")
        file.write("PROTECT DATA\n    0      \n")
        file.write("DATUM\n      0.00\n")
        file.write("RADIUS TYPE\n    0\n")
        file.write("DIVIDE X-Section\n0\n")
        file.write("SECTION ID\n     \n")
        file.write("INTERPOLATED\n    0\n")
        file.write("ANGLE\n    0.00   0\n")
        file.write(
            "RESISTANCE NUMBERS\n   1  0     1.000     1.000     1.000    1.000    1.000\n")
        file.write(f"PROFILE        {len(points)}\n")

        for i, point in enumerate(points):
            _, _, _, _, y, x = point
            file.write(
                f"     {float(x):f}     {float(y):1f}     1.000     <#1>     0     0.000     0\n")

        file.write("LEVEL PARAMS\n   0  0    0.000  0    0.000  50\n")
        file.write("*******************************\n")


# 调用函数进行转换
convert_csv_to_txt('BeiHengGang.csv', 'BeiHengGang.txt')
