import csv
import sys


def process_file(file_path, csv_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_branch = None
    chainage_count = 0

    for i, line in enumerate(lines):
        if i+3 < len(lines) and "COORDINATES" in lines[i+3]:
            new_branch = lines[i].strip()
            if new_branch != current_branch:
                current_branch = new_branch
                chainage_count = 0
                data[current_branch] = []

            chainage_number = lines[i+2].strip()
            data[current_branch].append((chainage_count, chainage_number))
            chainage_count += 1

    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Branch Name', 'Chainage', 'Number'])  # Header row

        for branch_name, chainages in data.items():
            for chainage in chainages:
                # Updated line
                formatted_chainage = f"chainage_{chainage[0]:02d}"
                csvwriter.writerow(
                    [branch_name, formatted_chainage, chainage[1]])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mks2chainage.py <input_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_csv_file = '../chainage.csv'  # You can modify this if needed
    process_file(input_file_path, output_csv_file)
    print(f"Processed file: {input_file_path}")

