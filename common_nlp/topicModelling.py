try:
	from textNormalization import textNormalization
except:
	from common_nlp.textNormalization import textNormalization
from gensim import corpora, models
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
import matplotlib.pyplot as plt
import subprocess, pickle, pandas as pd

#visualizations of topic_models extracted from: https://gist.github.com/tokestermw/3588e6fbbb2f03f89798

class topicModelling(textNormalization):
	"""Creates topic models for normalized texts"""
	def __init__(self):
		super(topicModelling, self).__init__()
	
	def dbscan_dados(self, topics, epsilon=0.5, num_topics=5, n_words=15):
		X = self.topics_to_vectorspace(topics, num_topics=num_topics, n_words=n_words)
		clustering = DBSCAN(eps=epsilon).fit(X.toarray())
		return clustering.labels_

	def dicionario_corpora(self,textos):
		return corpora.Dictionary(textos)

	def lda_Model(self, texts, num_topics=5, npasses=20):
		'''O input precisa ser uma lista em que cada elemento da lista é uma string correspondendo a um texto'''
		textos = self.normalize_texts(texts)
		dicionario = self.dicionario_corpora(textos)
		corpus = [dicionario.doc2bow(text) for text in textos]
		return models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dicionario, passes=npasses)

	def pca_topics(self, topics, name, n_components=2, num_topics=5, n_words=15):
		X = self.topics_to_vectorspace(topics, num_topics=num_topics, n_words=n_words)
		X_array = X.toarray()
		pca = PCA(n_components=n_components)
		X_pca = pca.fit(X_array).transform(X_array)
		plt.figure()
		for i in range(X_pca.shape[0]):
			plt.scatter(X_pca[i, 0], X_pca[i, 1], alpha=.5)
			plt.text(X_pca[i, 0], X_pca[i, 1], s=' ' + str(i))
		plt.title('PCA Topics of %s' % (name,))
		plt.savefig("pca_topics_%s.png" % (name,))
		plt.close()
		return X_pca

	def topic_to_txt(self, topics, nome_topicos='',num_topics=5,num_words=15):
		for n,top in topics.print_topics(num_topics=num_topics,num_words=num_words):
			arq = open('wordcloud_topico_'+str(n)+nome_topicos+'.txt','w')
			for t in top.split('+'):
				t = t.strip().replace('"','')
				n_t, word = t.split('*')
				arq.write(int(float(n_t)*1000)*(word+' '))
			subprocess.Popen('wordcloud_cli --text %s --imagefile wordcloud_%s.png --no_collocations' % ('wordcloud_topico_'+str(n)+nome_topicos+'.txt',str(n)+nome_topicos),shell=True)

	def topics_to_vectorspace(self, topics, num_topics=5, n_words=15):
		rows = []
		for i in range(num_topics):
			temp = topics.show_topic(i, n_words)
			row = dict(((i[1],i[0]) for i in temp))
			rows.append(row)
		vec = DictVectorizer()
		X = vec.fit_transform(rows)
		return X

if __name__ == '__main__':
	dados_1_inst = '/home/ubuntu/topicmodelling/relatorio_cnj_final_1_inst.csv' #texto_decisao
	dados_2_inst = '/home/ubuntu/topicmodelling/relatorio_cnj_final_2_inst_sp.csv' #texto_decisao
	dados_tutela = '/home/ubuntu/topicmodelling/publicacoes_saude.csv'

	def relatorio(path_dados, nome):
		tp = topicModelling()
		df = pd.read_csv(path_dados,chunksize=10, nrows=100)
		num_topics = 30
		npasses = 20
		dicionario = tp.dicionario_corpora([['direito']])
		topicos = models.ldamodel.LdaModel([['direito']], num_topics=num_topics, id2word = dicionario, passes=npasses)
		for chunk in df:
			textos = []
			for index, row in chunk.iterrows():
				paragrafos = row['texto_publicacao'].split('\n')
				for p in paragrafos:
					textos.append(p)
			textos_n = tp.normalize_texts(textos)
			dicionario.add_documents(textos_n)
		
		df = pd.read_csv(path_dados,chunksize=10, nrows=100)
		for chunk in df:
			textos = []
			for index, row in chunk.iterrows():
				paragrafos = row['texto_publicacao'].split('\n')
				for p in paragrafos:
					textos.append(p)
			textos_n = tp.normalize_texts(textos)
			corpus = [dicionario.doc2bow(text) for text in textos_n]
			topicos.update(corpus)
		pickle.dump(topicos,open('topicos_%s.pickle' % (nome,),'wb'))
	
	relatorio(dados_1_inst,'1_instancia_paragrafos')
	relatorio(dados_2_inst,'2_instancia_paragrafos')
	relatorio(dados_tutela,'tutela_paragrafos')