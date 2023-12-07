import sys
import pandas as pd
import os
import csv


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
    # Path to the directory where files will be saved
    output_dir = "../processed_data/chg_files/"
    # Check if the directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Path to the CSV file
    csv_file = '../processed_data/chainage.csv'
    # Validate the CSV file
    expected_columns = 5  # Update this number based on your requirement
    try:
        validate_csv(csv_file, expected_columns)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    # Read the original CSV file
    df = pd.read_csv(csv_file)
    # Group by the 'river' column
    grouped = df.groupby('river')
    # Counter for file numbering
    file_number = 1
    # Iterate over each group
    for name, group in grouped:
        # Construct the filename using the file number and the output directory
        filename = f"{output_dir}{file_number:02d}_{name}_chg.csv"
        # Write the group to a new CSV file
        group.to_csv(filename, index=False)
        # Increment the file number
        file_number += 1


if __name__ == "__main__":
    main()
