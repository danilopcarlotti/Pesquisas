from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd, pymongo, nltk

class active_learning_logreg():

    def __init__(self, N, K, threshold, csv_path, uri_mongo=None):
        # N is the number of elements that need to be classified initially for the classification to begin
        self.N = N
        # K is the number of elements that will be manually classified in each interation
        self.K = K
        # threshold is the minimum accuracy that the model should have before stopping the learning process
        self.threshold = threshold
        # csv_path is the path where the dataset can be found. The csv file should contain only one column, "raw_text"
        self.raw_texts = self.list_texts_raw(csv_path)
        # the texts are transformed in tfidf vectors
        self.normalized_texts_training = self.normalize_texts(self.raw_texts)
        # This database will be created in the mongodb at localhost
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient['active_learning_db']
        # This collection will be created in the mongodb
        self.doc_collection = self.mydb['document_classification_al']
        # Insert the processed documents in the database for future comparison
        self.insert_raw_texts(self.normalized_texts_training, self.raw_texts)
        # The model that will be constantly updated
        self.vect_fit = None
        self.current_model = None
        self.model_score = None
    
    def update_model(self):
        texts = []
        for doc in self.doc_collection.find({'class_human': {'$gt':-1}}):
            texts.append([doc['raw_text'],doc['class_human']])
        list_texts = self.normalize_texts(texts)
        vect = TfidfVectorizer()
        self.vect_fit = vect.fit([i[0] for i in list_texts])
        tfidf = self.vect_fit.transform([i[0] for i in list_texts])
        X = tfidf.A
        y = [i[1] for i in list_texts]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        self.current_model = LogisticRegression(solver='liblinear',penalty='l1')
        self.current_model.fit(X_train, y_train)
        self.model_score = self.current_model.score(X_test, y_test)
    
    def insert_raw_texts(self, normalized_texts, raw_texts):
        for t in range(len(normalized_texts)):
            self.doc_collection.insert_one({
                'raw_text':raw_texts[t],
                'tfidf_vector':normalized_texts[t],
                'class_human':-1,
                'class_machine':-1
            })

    def find_K_documents(self):
        texts = []
        for doc in self.doc_collection.find({'class_machine':-1}):
            texts.append(doc['raw_text'])
        list_texts = self.normalize_texts(texts)
        results = []
        for lt in list_texts:
            tfidf = self.vect_fit.transform([lt])
            X = tfidf.A
            results.append([lt,self.current_model.predict_proba(X)[0][1]]) # verificar esse resultado
        results.sort(key=lambda x:x[1])
        # processar os textos para ranquear e escolher os mais incertos tentando classificar com o modelo treinado
        # atribuir uma 'class_machine' para todos que puderem ser classificados com uma certeza maior que o threshold
        # sort a lista e pegar os primeiros K resultados
        middle = len(results)//2
        if middle > self.K:
            most_uncertain = [i[0] for i in results][middle-(self.K//2):middle+(self.K//2)]
        else:
            most_uncertain = [i[0] for i in results][middle-(middle//2):middle+(middle//2)]
        return most_uncertain

    def find_N_documents(self):
        texts = []
        for doc in self.doc_collection.find({}):
            if len(texts) < self.N:
                texts.append(doc['raw_text'])
            else:
                break
        return texts

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
        if one_text:
            return tokenized_text
        return normal_texts
    

input_al = 'csv with one column "raw_text"'

premissas = '''
    1) Base de dados aonde se conectar
    2) X elementos treinados inicialmente, sem ajuda
    3) A cada interação, classificar manualmente K elementos
    4) Threshold de certeza Z que o classificador deve ter para todos os elementos para parar o processo
'''

etapas = '''
    1) Treinar manualmente uma base de tamanho X
    2) Com base no que foi classificado, treinar novamente o classificador com os K novos inputs
    3) Verificar para todos os elementos existentes quais deles não foram classificados com a certeza mínima Z
    4) Classificar todos aqueles cuja certeza foi suficientemente grande e deixar separados. Se não houver 
    elementos, passar para o passo 7
    5) Disponibilizar os K elementos cuja classificação foi a mais incerta possível para o usuário
    6) Após reclassificação, voltar ao passo 3
    7) Exibir: o score da ferramenta de classificação, porcentagem de elementos classificados manualmente
'''

doc_collection = 'document_classification_al'

single_doc = {
    # '_id':'random'
    'tfidf_vector':'texto_processado_na_forma_de_vetor',
    'class_human':-1,
    'class_machine':-1
}

results = {
    'accuracy':0.0,
    'texts_manually_classified':0,
    'classification_ended':False
}