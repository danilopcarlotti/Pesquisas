from sklearn.feature_extraction.text import HashingVectorizer
import pymongo, numpy as np, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.getcwd()))))
from pesquisas.search_engine.mongo_url import mongo_url
from pesquisas.common.recursive_folders import recursive_folders
from pesquisas.common_nlp.textNormalization import textNormalization

class main_class():
    def __init__(self):
        self.myclient = pymongo.MongoClient(mongo_url)
        # self.DATABASE = 'jurisprudencia_se'
        self.DATABASE = 'banco_precos'
        # self.COLLECTION = 'covid'
        self.COLLECTION = '2019'
        self.COLLECTION_CLUSTERS = self.COLLECTION + '_cluster_'
        self.COLLECTION_INDEX = self.DATABASE+'_'+self.COLLECTION+'_index'
        # self.COLUMN_SOURCE = 'text'
        self.COLUMN_SOURCE = 'historico_despesa'
        self.ALTERNATE_COLUMN_SOURCE = ''
        self.VAR_NAME = 'vetor'
        self.NUMBER_OF_CLUSTERS = 10
        # self.NUMBER_OF_CLUSTERS = 1000
        self.N_FEATURES = 25000
        self.mydb = self.myclient[self.DATABASE]
        self.myclient = pymongo.MongoClient(mongo_url)
        self.vectorizer = HashingVectorizer(n_features=self.N_FEATURES,dtype=np.float32)
        # self.PATH = '/mnt/Dados/Documents/covid19/covid_2020_new.csv'
        self.PATH = '/mnt/Dados/Documents/pesquisas_privado_dados/compras_publicas/Portais_transparência/2019'
        self.txtN = textNormalization()
        self.rec = recursive_folders()
