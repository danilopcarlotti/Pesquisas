from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
try:
	from textNormalization import textNormalization
except:
	from common_nlp.textNormalization import textNormalization
import numpy as np
import pandas as pd 
import pickle

class vectorizer_texts_tfidf():

    def __init__(self, df_path, use_pca=True, N=1000, min_df=0.1, max_df=0.5, df_column_text='text',df_class_text='class', create_y=True):
        self.df = pd.read_csv(df_path)
        self.vectorizer = TfidfVectorizer(min_df=min_df, max_df=max_df)
        self.txtN = textNormalization()
        self.create_y = create_y
        self.create_X_y(df_column_text,df_class_text)
        self.use_pca = use_pca
        if use_pca:
            self.create_X_PCA(N=N)

    def create_X_y(self,df_column_text,df_class_text):
        self.normal_texts = [' '.join(i) for i in self.txtN.normalize_texts(self.df[df_column_text].tolist())]
        self.vectorizer.fit(self.normal_texts)
        self.tfidf = self.vectorizer.transform(self.normal_texts)
        self.X = [np.array(i).astype(np.float) for i in self.tfidf.A]
        if self.create_y:
            self.y = self.df[df_class_text].tolist()
    
    def create_X_PCA(self,N):
        self.pca = PCA(n_components=N, whiten=True)
        self.pca_vectorizer = self.pca.fit(self.X)
        self.X_pca = self.pca_vectorizer.transform(self.X)
    
    def dump_clf(self, prefix='', titulo=''):
        pickle.dump(self.vectorizer,open(prefix+'vectorizer%s.pickle' % (titulo,),'wb'))
        if self.use_pca:
            pickle.dump(self.pca_vectorizer,open(prefix+'pca_vectorizer%s.pickle' % (titulo,),'wb'))
            