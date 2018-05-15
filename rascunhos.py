from common_nlp.pdf_to_text import pdf_to_text
# from diarios_base import *
import os

contador = 0
arqs_i = os.listdir('/home/danilo/Documentos/Diários_trt_2017')
for arq in arqs_i:
	arq_trt = open("/home/danilo/Documentos/Diários_trt_2017_txt/trt{}.txt".format(str(contador)),'a',encoding="utf-8")
	arq_trt.write(pdf_2_txt.convert_pdfminer(i))
	contador += 1
	arq_trt.close()