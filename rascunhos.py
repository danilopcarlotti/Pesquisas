# from common.recursive_folders import recursive_folders
# from common_nlp.pdf_to_text import pdf_to_text

# pdf2txt = pdf_to_text()
# r = recursive_folders()
# paths = r.find_files('/home/danilo/Desktop/Parecer PL/')

# for arq in paths:
# 	texto = pdf2txt.convert_Tika(arq)
# 	arq_texto = open(arq.split('.')[0]+'.txt','w')
# 	arq_texto.write(texto)


from common.recursive_folders import recursive_folders
from common_nlp.topicModelling import topicModelling
from common_nlp.pdf_to_text import pdf_to_text
import pickle

pdf2txt = pdf_to_text()
r = recursive_folders()
paths_pareceres = r.find_files('/home/danilo/Desktop/Parecer PL/Pareceres e notas técnicas/')
paths_pl_fa = r.find_files('/home/danilo/Desktop/Parecer PL/PL forças armadas/')
paths_projetos_lei = r.find_files('/home/danilo/Desktop/Parecer PL/Projetos de lei e minutas/')
path_moraes = r.find_files('/home/danilo/Desktop/Parecer PL/Projeto Moraes/')

# def topicos(paths, nome_relatorio):
# 	tp = topicModelling()
# 	textos = []
# 	for arq in paths:
# 		if arq[-4:] != '.txt':
# 			texto = pdf2txt.convert_Tika(arq)
# 			textos.append(texto)
# 	topicos = tp.lda_Model(textos,num_topics=10,num_words=30)
# 	pickle.dump(topicos,open('topicos_%s.pickle' % (nome_relatorio,),'wb'))
# 	tp.topic_to_txt(topicos,nome_topicos=nome_relatorio)

# print('pareceres')
# topicos(paths_pareceres,'pareceres')
# print('forças armadas')
# topicos(paths_pl_fa,'projeto_forcas_armadas')
# print('projetos de lei')
# topicos(paths_projetos_lei,'projetos_de_lei')
# print('projeto do Moraes')
# topicos(path_moraes,'projetos_alexandre_moraes')

from gensim.models import Word2Vec
from common_nlp.stopwords_pt import stopwords_pt

stopw = stopwords_pt()
stopwords = stopw.stopwords()

def vetores(paths, nome_relatorio):
	textos = []
	for arq in paths:
		if arq[-4:] != '.txt':
			texto = pdf2txt.convert_Tika(arq)
			textos += [[i for i in texto.lower().split(' ') if len(i) > 3 and i not in stopwords]]
	model = Word2Vec(textos, min_count=5, size=150)
	model.save(nome_relatorio+'.bin')

def palavras_semelhantes(palavra,nome_relatorio):
	modelo = Word2Vec.load(nome_relatorio+'.bin')
	print(sorted(modelo.most_similar(palavra,topn=20),key=lambda x: abs(float(x[1])),reverse=True))

# # print('pareceres')
# # vetores(paths_pareceres,'pareceres')
# # print('forças armadas')
# # vetores(paths_pl_fa,'projeto_forcas_armadas')
# # print('projetos de lei')
# # vetores(paths_projetos_lei,'projetos_de_lei')
# print('projeto do Moraes')
# vetores(path_moraes,'projetos_alexandre_moraes')

palavra = 'cooperação'
print('pareceres')
try:
	palavras_semelhantes(palavra,'pareceres')
except:
	print(palavra, ' não consta no vocabulário')
print('pl forças armadas')
try:
	palavras_semelhantes(palavra,'projeto_forcas_armadas')
except:
	print(palavra, ' não consta no vocabulário')
print('projetos de lei')
try:
	palavras_semelhantes(palavra,'projetos_de_lei')
except:
	print(palavra, ' não consta no vocabulário')
print('projeto do Moraes')
try:
	palavras_semelhantes(palavra,'projetos_alexandre_moraes')
except:
	print(palavra, ' não consta no vocabulário')

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel

# documents = []
# texto_moraes = ''.join([line for line in open('/home/danilo/Desktop/Parecer PL/Projeto Moraes/50201.txt','r')])
# texto_moro = ''.join([line for line in open('/home/danilo/Desktop/Parecer PL/Projetos de lei e minutas/[22]-7887238_Anexo_VERSAO_FINAL_DO_PL_ANTICRIME.txt','r')])
# documents.append(texto_moraes)
# documents.append(texto_moro)
# tfidf = TfidfVectorizer().fit_transform(documents)
# pairwise_similarity = tfidf * tfidf.T
# print(pairwise_similarity)

# cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
# print(cosine_similarities)