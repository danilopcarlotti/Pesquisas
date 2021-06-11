from tikapp import TikaApp

# import pdftotext
import os
import pytesseract
import sys

from glob import glob
from PIL import Image
from pdf2image import convert_from_path


class pdf_to_text:
    """Converts pdf to text with TikaApp"""

    def __init__(self):
        pass

    def convert_Tika(self, fname):
        tika_client = TikaApp(
            file_jar=os.path.dirname(os.getcwd()) + "/common_nlp/tika-app-1.20.jar"
        )
        return tika_client.extract_only_content(fname)

    def convert_pdf_pytesseract(self, PDF_FILE_PATH):
        pages = convert_from_path(PDF_FILE_PATH)
        image_counter = 1
        for page in pages:
            filename = (
                PDF_FILE_PATH.replace(".pdf", "")
                + "_page_"
                + str(image_counter)
                + ".jpg"
            )
            page.save(filename, "JPEG")
            image_counter += 1
        filelimit = image_counter - 1
        # f = open(PDF_FILE_PATH.replace('.pdf','.txt'), "a")
        text_final = ""
        for i in range(1, filelimit + 1):
            filename = PDF_FILE_PATH.replace(".pdf", "") + "_page_" + str(i) + ".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace("-\n", "")
            text_final += text
            # f.write(text)
        # f.close()
        return text_final

    def transform_pdf(self, fname):
        texto = ""
        try:
            texto_aux = self.convert_Tika(fname)
            if len(texto):
                texto += "TEXTO TIKA\n\n\n"
                texto += texto_aux
        except Exception as e:
            print(e)
        try:
            texto_aux = self.convert_pdf_pytesseract(fname)
            if len(texto_aux):
                texto += "\n\n\nTEXTO OCR\n\n\n"
                texto += texto_aux
        except Exception as e:
            print(e)
        arq = open(fname.replace("pdf", "txt"), "w", encoding="utf-8")
        arq.write(texto)
        arq.close()


if __name__ == "__main__":
    path = sys.argv[1]
    p = pdf_to_text()
    lista_arquivos = glob(path + "/**/*.pdf", recursive=True)
    set_txts = set(glob(path + "/**/*.txt", recursive=True))
    for arq in lista_arquivos:
        if arq.replace("pdf", "txt") in set_txts:
            continue
        print(arq)
        texto = p.convert_Tika(arq)
        arq_txt = open(arq.replace(".pdf", ".txt"), "w")
        arq_txt.write(texto)
        arq_txt.close()
        # p.transform_pdf(arq)
