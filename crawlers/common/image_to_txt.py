from PIL import Image
import cv2 as cv
import numpy as np
import argparse, pytesseract, subprocess, time

class image_to_txt():
	"""docstring for image_to_txt"""
	def __init__(self):
		pass

	def captcha_image_to_txt(self,img = None):
		if not img:
			img = 'imagem.png'
		boundaries = [
			([5, 5, 155], [100, 100, 255]),
			([155,5,5],[255,100,100]),
			([20, 200, 20], [50, 255, 50]),
			([86, 31, 4], [220, 88, 50]),
			([25, 146, 190], [62, 174, 250]),
			([103, 86, 65], [145, 133, 128])
		]
		img = cv.imread(img)
		cont = 0
		for (lower, upper) in boundaries:
			lower = np.array(lower, dtype = "uint8")
			upper = np.array(upper, dtype = "uint8")
			mask = cv.inRange(img, lower, upper)
			output = cv.bitwise_and(img, img, mask = mask)
			cv.imwrite('imagem_processada%s.png' % str(cont), output)
			text = pytesseract.image_to_string(Image.open('imagem_processada%s.png' % str(cont))).replace(' ','').replace('\n','')
			cont += 1
			if text != '':
				return text
		return ''

if __name__ == '__main__':
	i = image_to_txt()
	print(i.captcha_image_to_txt())