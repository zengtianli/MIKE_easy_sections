# Desc: This script is used to combine all the txt files in txt_updated_files to one file combined.txt
# Author: Tianli Zeng
set -e

# Go to scripts folder
echo "📂 Changing directory to 00_scripts..."
cd 00_scripts

# According to chainage.csv file to insert the chainage in csv_sections and save the result at inserted_files
echo "🔗 Inserting chainage data..."
for file in ../csv_sections/*.csv; do 
    echo "📝 Processing $file..."
    python chg_insert.py "$file"; 
done

# According to inserted_files to clean the csv file and save the result at inst_cle_files
echo "🧹 Cleaning CSV files..."
for file in ../inserted_files/*.csv; do 
    echo "🧼 Cleaning $file..."
    python clean_csv.py "$file"; 
done

# According to inst_cle_files to convert the csv file to txt file and save the result at txt_files
echo "🔄 Converting CSV to TXT..."
for file in ../inst_cle_files/*.csv; do 
    echo "🔃 Converting $file to TXT..."
    python mkcc.py "$file"; 
done

# Handle virtual cross sections, first virtual_start.py, then virtual_end.py, finally virtual_end_update.py
# virtual_start.py read files in txt_files, and save the result at txt_virtual_start
echo "🚀 Handling virtual start sections..."
python virtual_start.py

# virtual_end.py read files in txt_virtual_start, and save the result at txt_virtual_end
echo "🏁 Handling virtual end sections..."
python virtual_end.py

# virtual_end_update.py read files in txt_virtual_end, and save the result at txt_updated_files
echo "🔄 Updating virtual end sections..."
python virtual_end_update.py

for file in ../txt_updated_files/*.txt; do
  sed -i '' '/^$/d' "$file"
done

# Combine all the txt files in txt_updated_files to one file combined.txt
echo "🔗 Combining all TXT files into one..."
# First go to txt_updated_files folder
cd ..

# Then combine all the txt files to one file combined.txt
if [ -f combined.txt ]; then
    echo "🗑️ Removing existing combined.txt..."
    rm combined.txt
fi

echo "📚 Combining TXT files..."
cat ./txt_updated_files/*.txt > combined.txt
echo "✅ Completed combining TXT files into combined.txt!"

