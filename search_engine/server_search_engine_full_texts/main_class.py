from sklearn.feature_extraction.text import HashingVectorizer
import pymongo, numpy as np, sys, os
from mongoURI import mongo_url
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from pesquisas.common.recursive_folders import recursive_folders
from pesquisas.common_nlp.textNormalization import textNormalization

class main_class():
    def __init__(self):
        self.myclient = pymongo.MongoClient(mongo_url)
        self.DATABASE = 'jurisprudencia_se'
        self.COLLECTION = 'covid'
        self.COLLECTION_CLUSTERS = self.COLLECTION + '_cluster_'
        self.COLLECTION_INDEX = self.DATABASE+'_'+self.COLLECTION+'_index'
        self.COLUMN_SOURCE = 'text'
        self.ALTERNATE_COLUMN_SOURCE = ''
        self.VAR_NAME = 'vetor'
        self.NUMBER_OF_CLUSTERS = 10
        # self.NUMBER_OF_CLUSTERS = 1000
        self.N_FEATURES = 25000
        self.mydb = self.myclient[self.DATABASE]
        self.myclient = pymongo.MongoClient(mongo_url)
        self.vectorizer = HashingVectorizer(n_features=self.N_FEATURES,dtype=np.float32)
        self.PATH = '/mnt/Dados/Documents/covid19/covid_2020_new.csv'
        self.txtN = textNormalization()
        self.rec = recursive_folders()
