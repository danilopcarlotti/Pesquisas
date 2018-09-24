class stopwords_pt():
	"""Stopwords for postuguese"""
	def __init__(self):
		pass

	def stopwords(self):
		try:
			stpwrds = open('stopwords_pt.txt','r')
		except:
			import os
			stpwrds = open(os.getcwd()+'/common_nlp/stopwords_pt.txt','r')
		return [line for line in stpwrds]
