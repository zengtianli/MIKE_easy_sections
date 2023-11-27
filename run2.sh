cd scripts
for file in ../csv_sections/*.csv; do python chg_insert.py "$file"; done
for file in ../inserted_files/*.csv; do python clean_csv.py "$file"; done
for file in ../inst_cle_files/*.csv; do python mkcc.py "$file"; done
python virtual_start.py
python virtual_end.py
python virtual_end_update.py
# cat ./txt_updated_files/*.txt > combined.txt
# if exitst, remove the file
cd ..
if [ -f combined.txt ]; then
		rm combined.txt
fi
cat ./txt_updated_files/*.txt > combined.txt



