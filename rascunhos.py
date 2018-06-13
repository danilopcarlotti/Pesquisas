from common_nlp.pdf_to_text import pdf_to_text
# from crawlers.diarios_base import *
import os

contador = 0
arqs_i = os.listdir('/home/danilo/Documents/Diários_trt_2017')
pdf_2_txt = pdf_to_text()
contador = 2345
for arq in arqs_i:
	contador -= 1
	if contador < 993:
		try:
			arq_trt = open("/home/danilo/Documents/Diários_trt_2017_txt/trt{}.txt".format(str(contador)),'a',encoding="utf-8")
			arq_trt.write(pdf_2_txt.convert_pdfminer('/home/danilo/Documents/Diários_trt_2017/'+arq))
			arq_trt.close()
			print(contador)
		except Exception as e:
			print(e)
			print(arq)