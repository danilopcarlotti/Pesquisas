from math import log2
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import nltk, pickle, re, random, os, sys
sys.path.append('../')
from common_nlp.classifier_legal_phrases import classify_sentences


PATH_CLASSIFIERS = os.path.join(os.path.dirname(os.getcwd()), 'common_nlp/', )

class summarization_texts():
    
    def __init__(self, raw_text):
        self.list_sentences_raw = self.sentences_raw(raw_text)
        self.list_sentences_sections = classify_sentences(raw_text,path_classifiers=PATH_CLASSIFIERS)
        self.tfidf_texts = self.normalize_texts()
        self.distance_matrix_tfidf = pairwise_distances(self.tfidf_texts, self.tfidf_texts, n_jobs=-1)
        self.N_iterations_steps = 10
        self.random_size = [i for i in range(5)]
        if len(self.list_sentences_raw) > 20:
            self.random_size += random.sample(range(5,len(self.list_sentences_raw)), 10)

    def genetic_search(self):
        best_summary = {}
        for rand in self.random_size:
            pool_summaries = []
            for i in range(self.N_iterations_steps):
                pool_summaries.append(self.genetic_search_step(rand, self.list_sentences_sections, self.list_sentences_sections)[1])
            best_summaries = []
            for p in pool_summaries:
                best_summaries += p
            best_summary[rand] = self.genetic_search_step(rand, best_summaries, self.list_sentences_sections)
        return best_summary

    def genetic_search_step(self, size_summary, list_sentences_indexes, list_sentences_sections):
        list_sentences_indexes = list(set(list_sentences_indexes))
        summaries = []
        for n in range(self.N_iterations_steps):
            summary = []
            indexes = random.sample(list_sentences_indexes, size_summary)
            for i in indexes:
                summary.append(i,list_sentences_sections[i])
            summaries.append(self.score_summary(summary),summary)
        summaries.sort(reverse=True,key=lambda x: x[0])
        return summaries[0]

    def normalize_texts(self):
        normal_texts = []
        tk = RegexpTokenizer(r'\w+')
        # stopwords = nltk.corpus.stopwords.words('portuguese')
        # stemmer = nltk.stem.RSLPStemmer()
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = SnowballStemmer("english")
        for t in self.list_sentences_raw:
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
        vect = TfidfVectorizer()
        self.vect_fit = vect.fit(normal_texts)
        tfidf = self.vect_fit.transform(normal_texts)
        return tfidf.A
    
    def sentences_raw(self, raw_text):
        return re.split(r'\w\.\s',raw_text)

    def score_between_sections(self, section_A, section_B):
        result = 0.0
        for index in section_A:
            for m in section_B:
                result += self.distance_matrix_tfidf[index][m]
        return result

    def score_entropy(self, sections_dict):
        entropy_dict = {}
        result = 0.0
        total_phrases = 0
        for k,v in sections_dict.items():
            entropy_dict[k] = len(v)
            total_phrases += len(v)
        for k,v in entropy_dict.items():
            result += (v/total_phrases)*log2(v/total_phrases)
        return -1*result

    def sections_dictionary(self, summary):
        sections = {}
        for index, section in summary:
            if section not in sections:
                sections[section] = []
            sections[section].append(index)
        return sections

    def score_summary(self, summary):
        sections = self.sections_dictionary(summary)
        score = 0.0
        for k,v in sections.items():
            score += self.score_between_sections(v,v)
        for section in sections:
            score_aux = 0.0
            for k,v in sections.items():
                if k != section:
                    score_aux += self.score_between_sections(sections[section], v)
            score -= score_aux
        score += self.score_entropy(sections)
        return score
