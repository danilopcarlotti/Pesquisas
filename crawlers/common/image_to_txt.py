from PIL import Image
import cv2 as cv
import numpy as np
import argparse, pytesseract, subprocess

class image_to_txt():
	"""docstring for image_to_txt"""
	def __init__(self):
		pass

	def captcha_image_to_txt(self,img = None, colors = 2):
		if not img:
			img = 'imagem.png'
		img = cv.imread(img,0)
		results = []
		thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)[1]
		cv.imwrite('imagem_processada_1.png', thresh1)
		text1 = pytesseract.image_to_string(Image.open('imagem_processada_1.png')).replace(' ','').replace('\n','')
		results.append(text1)
		if colors > 1:
			thresh2 = cv.threshold(img,80,200,cv.THRESH_TRUNC)[1]
			cv.imwrite('imagem_processada_2.png', thresh2)
			text2 = pytesseract.image_to_string(Image.open('imagem_processada_2.png')).replace(' ','').replace('\n','')
			results.append(text2)
		subprocess.Popen('rm imagem_processada*.png', shell=True)
		return results

if __name__ == '__main__':
	i = image_to_txt()
	print(i.captcha_image_to_txt())