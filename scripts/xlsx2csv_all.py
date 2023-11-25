import pandas as pd
import os


def xlsx_to_csv(xlsx_file_path, csv_file_path):
    # Read the Excel file
    df = pd.read_excel(xlsx_file_path)

    # Write to a CSV file
    df.to_csv(csv_file_path, index=False)


# Walking through the current directory and subdirectories
for dirpath, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.endswith('.xlsx'):
            # Constructing file paths
            xlsx_file_path = os.path.join(dirpath, filename)
            csv_file_path = xlsx_file_path.replace('.xlsx', '.csv')

            # Converting the file
            xlsx_to_csv(xlsx_file_path, csv_file_path)
            print(f"Converted '{xlsx_file_path}' to '{csv_file_path}'")

