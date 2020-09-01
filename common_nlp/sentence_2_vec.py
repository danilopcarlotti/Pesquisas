from gensim import models
from gensim.models.doc2vec import TaggedDocument
import pandas as pd, re, spacy, gensim

class sentence_2_vec():

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.corpus = []
        self.nlp = spacy.load('pt_core_news_sm')
        self.create_corpus()
    
    def break_sentences(self, text):
        text = re.sub(r'\s+',' ',text)
        # return re.split(r'\w\.\s',text)
        doc = self.nlp(text)
        return [sent.text for sent in doc.sents]

    def create_corpus(self):
        for _, row in self.df.iterrows():
            self.tag_doc(row['id'],row['text'])

    def tag_doc(self, id_text, text):
        list_sentences = self.break_sentences(text)
        counter = 1
        for i in range(0, len(list_sentences),len(list_sentences)//4):
            for j in range(i,i+len(list_sentences)//4):
                if j < len(list_sentences):
                    self.corpus.append(TaggedDocument(words=list_sentences[j].split(), tags=[counter,id_text]))
                else:
                    break
            counter += 1

    def train_model(self, model_path='model_sentence_2_vec.bin'):
        model = gensim.models.Doc2Vec(vector_size=300, window=5, min_count=5, workers=4, epochs=20)
        model.build_vocab(self.corpus)
        model.train(self.corpus, total_examples=model.corpus_count, epochs=model.iter)
        model.save(model_path)

if __name__ == "__main__":
    s = sentence_2_vec('texts_sentence_2_vec.csv')
    print('Criando corpus')
    print(100*'*')
    print(s.corpus)
    print(100*'*')
    print('Criando modelo')
    s.train_model()