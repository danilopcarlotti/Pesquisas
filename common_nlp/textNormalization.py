from collections import Counter
from gensim import corpora, models
from nltk.tokenize import RegexpTokenizer
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

	def normalize_texts(self,texts,one_text=False):
		normal_texts = []
		tk = self.tokenizer()
		stopwords = nltk.corpus.stopwords.words('portuguese')
		if one_text:
			texts = [texts]
		for t in texts:
			texto_bruto = t.lower()
			tokens = tk.tokenize(texto_bruto)
			texto_processado = []
			for tkn in tokens:
				if len(tkn) > 3 and tkn not in stopwords:
					try:
						float(tkn)
					except:
						texto_processado.append(tkn)
			normal_texts.append(texto_processado)
		if one_text:
			return texto_processado
		return normal_texts

	def dicionario_invertido_id_texto(self,dados):
		dicionario_i = {}
		for id_,texto in dados:
			dicionario_i_text = set(self.normalize_texts(texto,one_text=True))
			for w in dicionario_i_text:
				if w in dicionario_i:
					dicionario_i[w].append(id_)
				else:
					dicionario_i[w] = [id_]
		return dicionario_i

	def text_to_hist(self, text):
		list_words = self.normalize_texts(text, one_text=True)
		return dict(Counter(list_words))

	def tokenizer(self):
		return RegexpTokenizer(r'\w+')
