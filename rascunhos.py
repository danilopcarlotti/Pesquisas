from common_nlp.topicModelling import topicModelling
import pickle

dados_1_inst = pickle.load(open('topicos_1_instancia.pickle','rb'))
dados_2_inst = pickle.load(open('topicos_2_instancia.pickle','rb'))
dados_tutelas = pickle.load(open('topicos_tutela.pickle','rb'))

top = topicModelling()
# top.pca_topics(dados_tutelas, 'tutelas')
print(top.dbscan_dados(dados_tutelas))