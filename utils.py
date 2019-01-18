import dill
import nltk
from sklearn.externals import joblib

def tokenize(text, stem=False):
    stemmer = nltk.stem.RSLPStemmer()
    result = []

    def valid_word(word):
        def isdigit(d):
            return d.isdigit()
        return len(word) > 1 and not any(map(isdigit, word))

    for word in filter(valid_word, nltk.tokenize.word_tokenize(text, language='portuguese')):
        proc_word = word.lower()
        if stem:
            proc_word = stemmer.stem(proc_word)
        result.append(proc_word)
    return result

def dummy_fun(x):
    return x

def load_model(filename):
    model = joblib.load(filename) 
    return model