from textNormalization import textNormalization
from gensim import corpora, models
import subprocess, pickle, pandas as pd

class topicModelling(textNormalization):
	"""Creates topic models for normalized texts"""
	def __init__(self):
		super(topicModelling, self).__init__()
		
	def dicionario_corpora(self,textos):
		return corpora.Dictionary(textos)

	def lda_Model(self, texts, num_topics=5, npasses=20, num_words=15):
		'''O input precisa ser uma lista em que cada elemento da lista é uma string correspondendo a um texto'''
		textos = self.normalize_texts(texts)
		dicionario = self.dicionario_corpora(textos)
		corpus = [dicionario.doc2bow(text) for text in textos]
		return models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dicionario, passes=npasses).print_topics(num_topics=num_topics,num_words=num_words)

	def topic_to_txt(self, topics):
		for n,top in topics:
			arq = open('wordcloud_topico_'+str(n)+'.txt','w')
			for t in top.split('+'):
				t = t.strip().replace('"','')
				n_t, word = t.split('*')
				arq.write(int(float(n_t)*10000)*(word+' '))
			subprocess.Popen('wordcloud_cli --text %s --imagefile wordcloud_%s.png --no_collocations' % ('wordcloud_topico_'+str(n)+'.txt',str(n)),shell=True)

if __name__ == '__main__':
	dados_1_inst = '/home/ubuntu/topicmodelling/relatorio_cnj_final_1_inst.csv' #texto_decisao
	dados_2_inst = '/home/ubuntu/topicmodelling/relatorio_cnj_final_2_inst_sp.csv' #texto_decisao

	tp = topicModelling()

	print('comecei 2 inst')

	df = pd.read_csv(dados_2_inst)
	textos = []
	for index, row in df.iterrows():
		textos.append(row['texto_decisao'])
	topicos = tp.lda_Model(textos,num_topics=30,num_words=30)
	pickle.dump(topicos,open('topicos_2_inst.pickle','wb'))

	print('terminei 2 inst')
	print('comecei 1 inst')

	df = pd.read_csv(dados_1_inst, sep=';')
	textos = []
	for index, row in df.iterrows():
		textos.append(row['texto_decisao'])
	topicos = tp.lda_Model(textos,num_topics=30,num_words=30)
	pickle.dump(topicos,open('topicos_1_inst.pickle','wb'))