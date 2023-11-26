#!/bin/bash

# 假定脚本和相关Python脚本都在scripts目录中
cd scripts

# 1. 执行Python脚本，将所有xlsx文件转换为csv
echo "Converting xlsx to csv..."
python xlsx2csv_all.py

# 2. 复制特定的csv文件到csv_sections目录
echo "Copying specific csv files to csv_sections directory..."
mkdir -p ../csv_sections
find ../csv_files/ -name '*断面测量数据表.csv' | xargs -I {} cp {} ../csv_sections

# 3. 处理csv_sections目录中的所有csv文件
echo "Processing csv files in csv_sections directory..."
python csv_distill.py ../csv_sections/*.csv

# 4. 重命名csv_sections目录中的文件
echo "Renaming files in csv_sections directory..."
python csv_rn_cap.py

echo "All tasks completed."
