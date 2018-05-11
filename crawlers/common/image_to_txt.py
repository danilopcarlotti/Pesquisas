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
			([230, 5, 5], [255, 100, 100]), #blue
			([5,230,5],[100,255,100]), #green
			([5, 5, 230], [100, 100, 255]), #red
			([0, 0, 0], [150, 150, 150]), #black
			([180, 30, 180], [250, 60, 250]) #purple
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