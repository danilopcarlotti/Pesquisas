import pandas as pd, sys, numpy as np, pickle, pymongo, re, os
from bson.objectid import ObjectId
from main_class import main_class
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from pesquisas.search_engine.mongo_url import mongo_url
from pesquisas.common_nlp.remove_accents import remove_accents

class binary_search_inverted_index(main_class):
    def __init__(self):
        super(binary_search_inverted_index, self).__init__()

    def binary_search(self, text):
        res = []
        for w in remove_accents(text.lower()).split(' '):
            res_word = self.mydb[self.COLLECTION_INDEX].find_one({'_id':w})
            if res_word:
                res += res_word['documents']
        return set(res)

    def retrive_data(self, text, prefix=''):
        collection = self.mydb[self.COLLECTION]
        ids_documents = self.binary_search(text)
        try:
            rows = []
            for id_d in ids_documents:
                data = collection.find_one({'_id':ObjectId(id_d)})
                del data['_id']
                if data:
                    rows.append(data)
            # print('Quantidade de dados encontrados ',len(rows))
            df = pd.DataFrame(rows,index=[i for i in range(len(rows))])
            df.to_excel(prefix+text.replace(' ','_')+'.xlsx', index=False)
            return True
        except Exception as e:
            print(e)
            return False
