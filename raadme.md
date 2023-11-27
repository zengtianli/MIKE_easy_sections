# MIKE Easy Import Cross-Sections Program

This program is designed to streamline the process of importing cross-section data into the MIKE software. It consists of two main parts: `part1.sh` and `part2.sh`, with a manual operation required between them.

## Overview

- `part1.sh`: Converts .xlsx files to .csv, renames and organizes these files, and extracts chainage data.
- `part2.sh`: Inserts chainage data into .csv files, cleans and converts these files to .txt, handles virtual cross-sections, and combines all .txt files into one.

## Prerequisites

- Python installed on your system.
- Input .xlsx files and a `chainage.csv` file correctly formatted.

## Installation

Clone the repository or download the scripts to your local machine.

## Usage

### Part 1: Initial Data Preparation

1. **Convert XLSX to CSV and Extract Chainage**
   Run `part1.sh` to convert .xlsx files to .csv, copy relevant .csv files, rename them, and extract chainage data.

   ```bash
   ./part1.sh
   ```

### Manual Operation

After completing Part 1, you need to manually:

1. **Denote Cross-Sections Names in `chainage.csv`**: Identify and mark the names of the cross-sections.
2. **Separate Data by River Name**: Based on the river names in `chainage.csv`, divide the data into corresponding `_chg.csv` files in the `00_chg_files` directory.

### Part 2: Final Data Processing and Combining

1. **Insert Chainage and Process Data**
   Run `part2.sh` to insert chainage data, clean .csv files, convert them to .txt, handle virtual cross-sections, and combine all .txt files.

   ```bash
   ./part2.sh
   ```

## Scripts Description

### `part1.sh`

- 📂 Moves to the scripts directory.
- 🔄 Converts .xlsx files to .csv.
- 📁 Creates a directory for csv sections and copies relevant files.
- ✏️ Renames .csv files.
- 📊 Extracts chainage data.

### `part2.sh`

- 📂 Changes directory to `00_scripts`.
- 🔗 Inserts chainage data into .csv files.
- 🧹 Cleans CSV files.
- 🔄 Converts CSV files to TXT.
- 🚀 Handles virtual start sections.
- 🏁 Manages virtual end sections.
- 🔄 Updates virtual end sections.
- 📚 Combines all TXT files into one `combined.txt`.

## Notes

- Ensure that all file paths and names are correctly set according to your directory structure.
- It's crucial to perform the manual steps accurately for the script to function properly.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or bug fixes.

## License

MIT

## Contact

zengtianli1@126.com

