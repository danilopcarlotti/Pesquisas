import pandas as pd, sys, numpy as np, pickle, pymongo, re, os

from bson.objectid import ObjectId
from collections import Counter
from main_class import main_class
from mongo_url import mongo_url
from sklearn.feature_extraction.text import HashingVectorizer

class inverted_index(main_class):
    def __init__(self):
        self.SEP = ';'
        self.ENCODING = 'latin-1'

    def insert_files(self):
        files = [i for i in self.rec.find_files(self.PATH) if i[-3:] == 'csv']
        session = self.myclient.start_session()
        for f in files:
            print(f)
            df = pd.read_csv(f,sep=self.SEP, encoding=self.ENCODING)
            df[self.COLUMN_SOURCE] = df[self.COLUMN_SOURCE].astype(str)
            for _, row in df.iterrows():
                if len(row[self.COLUMN_SOURCE]) > 10:
                    document_id = ObjectId()
                    normal_tokens = self.txtN.normalize_texts(row[self.COLUMN_SOURCE],one_text=True)
                    counter_f = Counter(normal_tokens)
                    # normal_text = ' '.join(normal_tokens)
                    # X = [float(i) for i in list(vectorizer.transform([normal_text]).toarray()[0])]
                    dic_aux = {}
                    for c in df.columns:
                        dic_aux[c] = row[c]
                    # dic_aux['vetor'] = X
                    dic_aux['_id'] = document_id
                    self.mydb[self.COLLECTION].insert_one(dic_aux)
                    self.insert_words_index(counter_f, self.mydb[self.COLLECTION_INDEX], document_id)
            self.myclient.admin.command('refreshSessions', [session.session_id], session=session)

    def insert_words_index(self, counter_f, collection, document_id):
        for word in counter_f:
            found_word = collection.find_one({'_id':word})
            if found_word:
                collection.update_one({'_id':word},{'$push':{
                    'documents':document_id
                }})
            else:
                collection.insert_one({
                    '_id':word,
                    'documents':[document_id]
                })

    def update_index(self):
        for d in self.mydb[self.COLLECTION].find({}):
            normal_tokens = self.txtN.normalize_texts(d[self.COLUMN_SOURCE],one_text=True)
            counter_f = Counter(normal_tokens)
            self.insert_words_index(counter_f, self.mydb[self.COLLECTION_INDEX], d['_id'])
