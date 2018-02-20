from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
import gensim, nltk

class textNormalization():
	"""Manipula topic models"""
	def __init__(self):
		pass

	def escape_text_insert(self,text):
		return text.replace('"','').replace('/','').replace('\\','').replace('<','').replace('>','')

	def file_to_string(self,arq):
		arquivo = open(arq,'r')
		return ''.join([line for line in arquivo])
	
	def month_name_number(self,text):
		text = text.lower()
		if text == 'janeiro':
			return '01'
		elif text == 'fevereiro':
			return '02'
		elif text == 'março':
			return '03'
		elif text == 'abril':
			return '04'
		elif text == 'maio':
			return '05'
		elif text == 'junho':
			return '06'
		elif text == 'julho':
			return '07'
		elif text == 'agosto':
			return '08'
		elif text == 'setembro':
			return '09'
		elif text == 'outubro':
			return '10'
		elif text == 'novembro':
			return '09'
		elif text == 'dezembro':
			return '12'

	def normalize_texts(self,texts):
		normal_texts = []
		tk = self.tokenizer()
		stopwords = nltk.corpus.stopwords.words('portuguese')
		for t in texts:
			texto_bruto = t.lower()
			tokens = tk.tokenize(texto_bruto)
			texto_processado = []
			for tkn in tokens:
				if tkn not in stopwords:
					texto_processado.append(tkn)
			normal_texts.append(texto_processado)
		return normal_texts

	def tokenizer(self):
		return RegexpTokenizer(r'\w+')
