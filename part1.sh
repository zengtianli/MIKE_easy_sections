# Desc: Convert xlsx to csv, rename the csv files, extract the chainage of the sections
# Author: Tianli Zeng
set -e

echo "🚀 Starting the script..."

# Go to the directory of the script
echo "📂 Moving to scripts directory..."
cd 00_scripts

# Walk through the directories to convert xlsx to csv
echo "🔄 Converting .xlsx files to .csv files..."
python xlsx2csv_all.py

# Create csv_sections directory and copy all the csv files with 断面测量数据表.csv to csv_sections
echo "📁 Creating directory for csv sections..."
mkdir -p ../csv_sections
echo "🔍 Finding and copying relevant .csv files..."
find ../csv_files/ -name '*断面测量数据表.csv' | xargs -I {} cp {} ../csv_sections

# Rename the csv files in csv_sections, rule is to capitalize the first letter of the file name
echo "✏️ Renaming .csv files..."
python csv_rn_cap.py

# Read MIKE txt file and extract the chainage of the sections
echo "📊 Extracting chainage data from MIKE txt file..."
python mks2chainage.py ../secss.txt

echo "✅ Script execution completed!"

