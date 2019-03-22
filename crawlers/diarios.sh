# !/bin/bash

path_download=$1
download_path_diarios=$2
data=$(date +'%Y%m%d')

python3 diarios_download.py
mv $path_download/*.pdf $download_path_diarios
python3 $diarios_pdf_txt.py $data
python3 diarios_csv.py $download_path_diarios