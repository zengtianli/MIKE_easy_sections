import sys
import pandas as pd
import os
import csv
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def validate_csv(file_path, expected_columns):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        if len(header) != expected_columns:
            raise ValueError(
                f"CSV header does not have the expected {expected_columns} columns.")
        # Start counting rows from 2 (header is row 1)
        for row_number, row in enumerate(reader, start=2):
            if len(row) != expected_columns:
                raise ValueError(
                    f"Row {row_number} does not have the expected {expected_columns} columns.")


def main():
    output_dir = os.path.join(BASE_DIR, 'processed_data', 'chg_files')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file = os.path.join(BASE_DIR, 'processed_data', 'chainage.csv')
    expected_columns = 5
    try:
        validate_csv(csv_file, expected_columns)
    except ValueError as e:
        raise ValueError(f"CSV file validation failed: {e}")

    df = pd.read_csv(csv_file)
    grouped = df.groupby('river')
    file_number = 1
    for name, group in grouped:
        filename = os.path.join(
            output_dir, f"{name}_chg.csv")
        group.to_csv(filename, index=False)
        file_number += 1


if __name__ == "__main__":
    main()
