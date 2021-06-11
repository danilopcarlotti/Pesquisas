import hashlib
import glob
import numpy as np
import pandas as pd
import pytesseract
import os
import sys
import cv2


from pdf2image import convert_from_path
from PIL import Image

hash_l = hashlib.sha256()


def convert_pdf_pytesseract(PDF_FILE_PATH):
    pages = convert_from_path(PDF_FILE_PATH)
    image_counter = 1
    for page in pages:
        filename = (
            PDF_FILE_PATH.replace(".pdf", "") + "_page_" + str(image_counter) + ".jpg"
        )
        page.save(filename, "JPEG")
        image_counter += 1
    filelimit = image_counter - 1
    text_final = ""
    for i in range(1, filelimit + 1):
        filename = PDF_FILE_PATH.replace(".pdf", "") + "_page_" + str(i) + ".jpg"
        img_clean = cv2.imread(filename)
        text = pytesseract.image_to_string(img_clean)
        text = text.replace("-\n", "")
        text_final += text
    return text_final


def convert_Tika(PDF_FILE_PATH, pdf_tika):
    texto = pdf_tika.convert_Tika(PDF_FILE_PATH)
    return texto


def hash_string(texto):
    return hashlib.md5("{}".format(texto).encode()).hexdigest()


if __name__ == "__main__":
    file_list = glob.glob(sys.argv[1] + "/*.pdf")
    # file_list = [line for line in open("/root/selecao_txts_processamento/txts_para_gerar.txt","r")]
    # df = pd.read_csv("informações_documentos_guias_unknowns.csv")
    # file_list = df["texto_ocr_fase_1"]
    rows = []
    counter = len(file_list)
    for PDF_FILE_PATH in file_list:
        print("Faltam {} por cento ".format(counter / len(file_list)))
        try:
            text = convert_pdf_pytesseract(PDF_FILE_PATH)
            arq = open(PDF_FILE_PATH.replace(".pdf", ".txt"), "w")
            arq.write(text)
            arq.close()
            counter -= 1
        except Exception as e:
            print(e)
    #     try:
    #         rows.append(convert_pdf_pytesseract_validations(PDF_FILE_PATH))
    #     except:
    #         pass
    # df = pd.DataFrame(rows)
    # df.to_csv("validação_formas_ocr_unknowns.csv", index=False)
