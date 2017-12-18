class stopwords_pt():
	"""Stopwords for postuguese"""
	def __init__(self):
		pass

	def stopwords(self):
		stpwrds = open('stopwords_pt.txt','r')
		return [line for line in stpwrds]
