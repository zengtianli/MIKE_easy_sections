import sys


def get_header_value(csv_path):
    """从CSV文件的第一行中提取头部值"""
    with open(csv_path, 'r') as csv_file:
        first_line = csv_file.readline().strip()
    return first_line


def parse_csv_line(line):
    """解析CSV文件中的一行，返回坐标值"""
    parts = line.split(',')
    x, y = parts[5].strip(), parts[4].strip()
    return float(x), float(y)  # 转换为浮点数以便于比较


def assign_tags(coordinates):
    """为坐标点分配标签"""
    if not coordinates:
        return []
    min_x = min(coordinates, key=lambda c: c[0])
    max_x = max(coordinates, key=lambda c: c[0])
    min_y = min(coordinates, key=lambda c: c[1])
    tagged_coords = []
    for x, y in coordinates:
        if (x, y) == min_x:
            tag = "<#1>"  # 最左岸
        elif (x, y) == max_x:
            tag = "<#4>"  # 最右岸
        elif (x, y) == min_y:
            tag = "<#2>"  # 最低点
        else:
            tag = "<#0>"  # 其他点
        tagged_coords.append((x, y, tag))
    return tagged_coords


def format_txt_section(header_value, chainage, coordinates):
    """将提取的数据格式化为TXT文件所需的格式，使用提取的头部值"""
    formatted_lines = [
        header_value,
        header_value,
        f"             {chainage}",
        "COORDINATES",
        "    0",
        # 其他静态文本内容
        "FLOW DIRECTION",
        "    0",
        "PROTECT DATA",
        "    0",
        "DATUM",
        "      0.00",
        "RADIUS TYPE",
        "    0",
        "DIVIDE X-Section",
        "0",
        "SECTION ID",
        " ",
        "INTERPOLATED",
        "    0",
        "ANGLE",
        "    0.00   0",
        "RESISTANCE NUMBERS",
        "   1  0     1.000     1.000     1.000    1.000    1.000",
        "PROFILE        3",
    ]
    for x, y, tag in coordinates:
        formatted_lines.append(
            f"     {x}     {y}     1.000     {tag}     0     0.000     0")
    formatted_lines.append("LEVEL PARAMS")
    formatted_lines.append("   0  0    0.000  0    0.000  50")
    formatted_lines.append("*******************************")
    return '\n'.join(formatted_lines)


def add_virtual_section_if_needed(chainage_value, txt_file, header_value):
    """如果需要，在河段的开始或结束添加虚拟断面，并确保chainage值和坐标值保留3位小数"""
    # 格式化chainage值以保持3位小数
    formatted_chainage = "{:.3f}".format(float(chainage_value))
    # 创建虚拟断面的坐标，确保坐标也保持3位小数
    virtual_coordinates = [
        ("{:.3f}".format(0), "{:.3f}".format(1), "<#1>"),
        ("{:.3f}".format(1), "{:.3f}".format(0), "<#2>"),
        ("{:.3f}".format(2), "{:.3f}".format(1), "<#4>")
    ]
    virtual_section = format_txt_section(
        header_value, formatted_chainage, virtual_coordinates)
    txt_file.write(virtual_section)
    txt_file.write("*******************************\n")  # 添加分隔符

def convert_csv_to_txt(csv_path, txt_path):
    header_value = get_header_value(csv_path)  # 获取CSV头部值
    with open(csv_path, 'r') as csv_file, open(txt_path, 'w') as txt_file:
        lines = csv_file.readlines()
        total_lines = len(lines)
        i = 1  # 从第二行开始，因为第一行已被读取
        while i < total_lines:
            if lines[i].startswith('chainage'):
                _, chainage_number, chainage_value = lines[i].split(',')
                chainage_value = chainage_value.strip()

                # 检查是否是文件的最后一行
                is_last_line = i == total_lines - 1

                # 如果是chainage 0或最后一行，添加虚拟断面
                if chainage_value == "0" or is_last_line:
                    add_virtual_section_if_needed(
                        chainage_value, txt_file, header_value)
                    if chainage_value == "0":
                        i += 1  # 跳过下一个实际的chainage为0的数据，避免重复
                    if is_last_line:
                        break  # 跳出循环，防止重复添加虚拟断面
                    continue

                coordinates = []
                i += 1  # 跳过标题行
                while i < total_lines and lines[i].strip() and not lines[i].startswith('chainage'):
                    coordinates.append(parse_csv_line(lines[i]))
                    i += 1

                tagged_coordinates = assign_tags(coordinates)
                section = format_txt_section(
                    header_value, chainage_value, tagged_coordinates)
                txt_file.write(section + '\n')

            else:
                i += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: python mk_cc.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    txt_file = csv_file.replace('.csv', '.txt')
    convert_csv_to_txt(csv_file, txt_file)
    print(f"Converted {csv_file} to {txt_file}")
if __name__ == "__main__":
    main()
