from textNormalization import textNormalization
from gensim import corpora, models

class topicModel(textNormalization):
	"""Creates topic models for normalized texts"""
	def __init__(self):
		super(topicModel, self).__init__()
		
	def dicionario_corpora(self,textos):
		return corpora.Dictionary(textos)

	def lda_Model(self, texts, num_topics=5, npasses=20, num_words=15):
		'''O input precisa ser uma lista em que cada elemento da lista é uma string correspondendo a um texto'''
		textos = self.processar_textos(texts)
		dicionario = self.dicionario_corpora(textos)
		corpus = [dicionario.doc2bow(text) for text in textos]
		return gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dicionario, passes=npasses).print_topics(num_topics=num_topics,num_words=num_words)

