from PIL import Image
import cv2 as cv
import numpy as np
import argparse, pytesseract, subprocess

class image_to_txt():
	"""docstring for image_to_txt"""
	def __init__(self):
		pass

	def captcha_image_to_txt(self,img = None):
		if not img:
			img = 'imagem.png'
		boundaries = [
			([17, 15, 100], [50, 56, 200]),
			([86, 31, 4], [220, 88, 50]),
			([25, 146, 190], [62, 174, 250]),
			([103, 86, 65], [145, 133, 128])
		]
		img = cv.imread(img,0)
		for (lower, upper) in boundaries:
			lower = np.array(lower, dtype = "uint8")
			upper = np.array(upper, dtype = "uint8")
			mask = cv.inRange(img, lower, upper)
			output = cv.bitwise_and(img, img, mask = mask)
			cv.imwrite('imagem_processada.png', output)
			text = pytesseract.image_to_string(Image.open('imagem_processada_.png')).replace(' ','').replace('\n','')
			if text != '':
				return text
		return ''

		# results = []
		# thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)[1]
		# cv.imwrite('imagem_processada_1.png', thresh1)
		# text1 = pytesseract.image_to_string(Image.open('imagem_processada_1.png')).replace(' ','').replace('\n','')
		# if text1 != '':
		# 	results.append(text1)
		# thresh2 = cv.threshold(img,80,200,cv.THRESH_TRUNC)[1]
		# cv.imwrite('imagem_processada_2.png', thresh2)
		# text2 = pytesseract.image_to_string(Image.open('imagem_processada_2.png')).replace(' ','').replace('\n','')
		# if text2 != '':
		# 	results.append(text2)
		# subprocess.Popen('rm imagem_processada*.png', shell=True)
		# return results

if __name__ == '__main__':
	i = image_to_txt()
	print(i.captcha_image_to_txt())