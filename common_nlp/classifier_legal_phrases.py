from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.pt.examples import sentences 
from scipy.spatial import distance
import pickle, pandas as pd, numpy as np, matplotlib.pyplot as plt, re, sys, spacy
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
try:
	from textNormalization import textNormalization
except:
	from common_nlp.textNormalization import textNormalization

class classifier_legal_phrases():
	"""classifier_legal_phrases """
	def __init__(self, list_texts_control, treshold_distance=None):
		self.list_texts_control = list_texts_control
		self.vectorizer = TfidfVectorizer()
		self.txtN = textNormalization()
		self.normal_texts = [' '.join(i) for i in self.txtN.normalize_texts(self.list_texts_control)]
		self.vect_fit = self.vectorizer.fit(self.normal_texts)
		self.X_control = self.vect_fit.transform(self.normal_texts).A
		if treshold_distance:
			self.treshold_distance = treshold_distance
		else:
			self.treshold_distance = np.mean(distance.cdist(self.X_control,self.X_control,'cosine'))

	def belongs_to_class(self,text):
		normal_txt = self.txtN.normalize_texts([text])
		tfidf_matrix = self.vect_fit.transform([' '.join(i) for i in normal_txt]).A
		smallest_dist = 1
		for x in self.X_control:
			mean_distance = np.mean(distance.cdist([x],tfidf_matrix,'cosine'))
			if mean_distance < smallest_dist and mean_distance <= self.treshold_distance/2:
				smallest_dist = mean_distance
		if smallest_dist < 1:
			return smallest_dist
		else:
			return False

def closest_n_index(X, n_c=10):
	kmeans = KMeans(n_clusters=n_c, random_state=0).fit(X)
	closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
	return closest

def closest_n_texts(residual_texts, n_c=10):
	txtN = textNormalization()
	normal_texts = [' '.join(i) for i in txtN.normalize_texts(residual_texts)]
	vect = TfidfVectorizer(min_df=5)
	tfidf = vect.fit_transform(normal_texts)
	X = tfidf.A
	closest = closest_n_index(X, n_c=n_c)
	representative_texts = []
	for i in closest:
		representative_texts.append(residual_texts[i])
	return representative_texts

def create_classifier(class_name, df_path='texts_manually_classified.csv'):
	df = pd.read_csv(df_path)
	list_of_texts = df[df['class_text'] == class_name]['phrase'].tolist()
	rel_ph = classifier_legal_phrases(list_of_texts)
	pickle.dump(rel_ph,open('classifier_phrases_%s.pickle' % (class_name,),'wb'))

def break_sentences(text, nlp):
	# return re.split(r'\w\.\s',text)
	text = re.sub(r'\s+',' ',text)
	doc = nlp(text)
	return [sent.text for sent in doc.sents]

def classify_text(text, nlp=None):
	if not nlp:
		nlp = spacy.load('en_core_web_sm')
	# USING CLASSIFIER
	classifier_facts = pickle.load(open('classifier_phrases_fact.pickle','rb'))
	classifier_claim = pickle.load(open('classifier_phrases_claim.pickle','rb'))
	classifier_decision = pickle.load(open('classifier_phrases_decision.pickle','rb'))
	classifier_laws = pickle.load(open('classifier_phrases_law.pickle','rb'))
	facts = []
	claims = []
	laws = []
	arguments = []
	decisions = []

	for sentence in break_sentences(text_to_analyse, nlp):
		res_facts = classifier_facts.belongs_to_class(sentence)
		res_claim = None
		res_decisions = None
		res_laws = None
		if res_facts:
			facts.append([sentence,res_facts])
		else:
			res_claim = classifier_claim.belongs_to_class(sentence)
			if res_claim:
				claims.append([sentence,res_claim])
			else:
				res_decisions = classifier_decision.belongs_to_class(sentence)
				if res_decisions:
					decisions.append([sentence,res_decisions])
				else:
					res_laws = classifier_laws.belongs_to_class(sentence)
					if res_laws:
						laws.append([sentence,res_laws])
		if not res_laws and not res_decisions and not res_claim and not res_facts:
			arguments.append(sentence)
	
	# typical_arguments = closest_n_texts(arguments, n_c=n_c)
	typical_arguments = arguments
	facts.sort(key=lambda x:x[1])
	claims.sort(key=lambda x:x[1])
	decisions.sort(key=lambda x:x[1])
	laws.sort(key=lambda x:x[1])
	dic_aux = {
		'Facts':facts[:n_c],
		'claims':claims[:n_c],
		'Decisions':decisions[:n_c],
		'Laws':laws[:n_c],
		'Arguments':typical_arguments[:n_c]
	}
	return dic_aux

def classify_sentences(text, path_classifiers='', nlp=None):
	if not nlp:
		nlp = spacy.load('pt_core_news_sm')

	dictionary_methods = {
		'fact':pickle.load(open(path_classifiers+'classifier_phrases_fact.pickle','rb')),
		'claim':pickle.load(open(path_classifiers+'classifier_phrases_claim.pickle','rb')),
		'decision':pickle.load(open(path_classifiers+'classifier_phrases_decision.pickle','rb')),
		'law':pickle.load(open(path_classifiers+'classifier_phrases_law.pickle','rb'))
	}

	classes_sentences = []

	for sentence in break_sentences(text, nlp):
		sentence_found = False
		for k,v in dictionary_methods.items():
			if v.belongs_to_class(sentence):
				classes_sentences.append(k)
				sentence_found = True
				break
		if not sentence_found:
			classes_sentences.append('argument')
	return classes_sentences

if __name__ == '__main__':
	
	# # CREATE CLASSIFIERS
	# classes = ['fact','claim','decision','law']
	# for c in classes:
	# 	create_classifier(c)
	# sys.exit()

	text_to_analyse = sys.argv[1]
	language = sys.argv[2]
	
	if language == 'pt':
		nlp = spacy.load('pt_core_news_sm')
	elif language == 'en':
		nlp = spacy.load('en_core_web_sm')
	else:
		raise('Language not supported')
	