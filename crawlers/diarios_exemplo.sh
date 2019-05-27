#!/bin/bash

python3.5 diarios_download.py
mv path_download/*.pdf download_path_diarios/*.pdf
python3.5 diarios_pdf_txt.py
python3.5 diarios_base.py