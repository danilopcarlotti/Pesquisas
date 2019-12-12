from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd, pymongo, nltk, pickle, os, numpy as np

DATABASE_NAME = 'active_learning_db'
COLLECTION_NAME = 'document_classification_al'
PATH_MODEL = os.getcwd()

class active_learning_logreg():

    def __init__(self, N, K, threshold_delta, csv_path, path_model_save=PATH_MODEL, uri_mongo=None):
        # N is the number of elements that need to be classified initially for the classification to begin
        self.N = N
        # K is the number of elements that will be manually classified in each interation
        self.K = K
        # threshold_delta is the minimum accuracy that the model should have (difference between 0.5 and the desired)
        # before stopping the learning process
        self.threshold_delta = threshold_delta
        # csv_path is the path where the dataset can be found. The csv file should contain only one column, "raw_text"
        self.raw_texts = self.list_texts_raw(csv_path)
        # the texts are transformed in tfidf vectors
        self.normalized_texts_training = self.normalize_texts(self.raw_texts)
        # This database will be created in the mongodb at localhost
        if not uri_mongo:
            uri_mongo = "mongodb://localhost:27017/"
        self.myclient = pymongo.MongoClient(uri_mongo)
        self.mydb = self.myclient[DATABASE_NAME]
        # This collection will be created in the mongodb
        self.doc_collection = self.mydb[COLLECTION_NAME]
        # Insert the processed documents in the database for future comparison
        self.insert_raw_texts()
        # The model that will be constantly updated
        self.vect_fit = None
        self.current_model = None
        self.model_score = None
        self.path_model_save = path_model_save

    def classify_texts(self):
        for doc in self.doc_collection.find({'class_human':{'$gt':-1}}):
            class_prediction = self.current_model.predict([doc['tfidf_vector']])[0]
            self.doc_collection.update_one({'_id':doc['_id']},{
                'class_machine':class_prediction
            })

    def dump_model(self):
        pickle.dump( self.current_model, open(self.path_model_save+'active_learning_model.pickle','wb'))

    def find_K_documents(self):
        X = []
        for doc in self.doc_collection.find({'class_machine':-1}):
            X.append((doc['tfidf_vector'],doc['_id']))
        results = []
        if not len(X):
            return False
        for doc_v, _id in X:
            results.append([_id, self.current_model.predict_proba([doc_v])[0][1]]) # verificar esse resultado!!
        most_uncertain = [i[0] for i in results if (i[1] < 0.5 + self.threshold_delta and i[1] > 0.5 - self.threshold_delta)][:self.K]
        # update documents with to_classify to 1

    def find_N_documents(self):
        texts = []
        for doc in self.doc_collection.find({}):
            # update document with to_classify to 1
            pass

    def insert_raw_texts(self):
        for t in range(len(self.normalized_texts_training)):
            self.doc_collection.insert_one({
                'raw_text':self.raw_texts[t],
                'tfidf_vector':self.normalized_texts_training[t],
                'class_human':-1,
                'class_machine':-1,
                'to_classify':0
            })

    def list_texts_raw(self, csv_path):
        df_raw = pd.read_csv(csv_path, usecols=['raw_text'])
        df_raw = df_raw.sample(frac=1).reset_index(drop=True)
        return df_raw['raw_text']
    
    def normalize_texts(self,texts,one_text=False):
        normal_texts = []
        tk = RegexpTokenizer(r'\w+')
        # stopwords = nltk.corpus.stopwords.words('portuguese')
        # stemmer = nltk.stem.RSLPStemmer()
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = SnowballStemmer("english")
        if one_text:
            texts = [texts]
        for t in texts:
            raw_text = t.lower()
            tokens = tk.tokenize(raw_text)
            tokenized_text = []
            for tkn in tokens:
                tkn = stemmer.stem(tkn)
                if tkn not in stopwords:
                    try:
                        float(tkn)
                    except:
                        tokenized_text.append(tkn)
            normal_texts.append(tokenized_text)
        # return normal_texts
        # tfidf dos textos
        vect = TfidfVectorizer()
        self.vect_fit = vect.fit(normal_texts)
        tfidf = self.vect_fit.transform(normal_texts)
        return tfidf.A
    
    def stop_model_check(self):
        class_human = []
        class_machine = []
        for doc in self.doc_collection.find({'class_machine': {'$gt':-1}}):
            class_human.append(doc['class_human'])
            class_machine.append(doc['class_machine'])
        results = []
        for i in range(len(class_human)):
            if class_human[i] == class_machine[i]:
                results.append(1)
            else:
                results.append(0)
        if np.mean(results) > 0.5 + self.threshold_delta:
            return True
        else:
            return False

    def update_model(self):
        X = []
        y = []
        for doc in self.doc_collection.find({'class_human': {'$gt':-1}}):
            X.append(doc['tfidf_vector'])
            y.append(doc['class_human'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
        self.current_model = LogisticRegression(solver='liblinear', penalty='l1')
        self.current_model.fit(X_train, y_train)
        self.model_score = self.current_model.score(X_test,y_test)
        self.classify_texts()

if __name__ == "__main__":
    actv_lrn = active_learning_logreg(20, 10, 0.4, 'csv_path.csv')
    
    actv_lrn.find_N_documents()
    # classify them manually and update documents

    # while Documents to classify
    while True:
        docx_to_classify = actv_lrn.find_K_documents()
        # classify them manually and update document
        actv_lrn.update_model()
        if actv_lrn.stop_model_check():
            break
    # print(actv_lrn.model_score)
    actv_lrn.dump_model()