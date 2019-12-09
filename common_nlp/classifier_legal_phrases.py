from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.pt.examples import sentences 
from scipy.spatial import distance
from textNormalization import textNormalization
import pickle, pandas as pd, numpy as np, re, sys, spacy
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

class classifier_legal_phrases():
	"""classifier_legal_phrases """
	def __init__(self, list_texts_control, nlp, treshold_distance=None):
		self.list_texts_control = list_texts_control
		self.vectorizer = TfidfVectorizer()
		self.txtN = textNormalization()
		self.nlp = nlp
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
	closest, aux = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
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

def create_classifier(class_name, nlp, df_path='texts_manually_classified.csv'):
	df = pd.read_csv(df_path)
	list_of_texts = df[df['class_text'] == class_name]['phrase'].tolist()
	rel_ph = classifier_legal_phrases(list_of_texts, nlp)
	pickle.dump(rel_ph,open('classifier_phrases_%s.pickle' % (class_name,),'wb'))

def break_sentences(text, nlp):
	doc = nlp(text)
	return [sent.text for sent in doc.sents]

if __name__ == '__main__':
	language = sys.argv[1]
	
	if language == 'pt':
		nlp = spacy.load('pt_core_news_sm')
	elif language == 'en':
		nlp = spacy.load('en_core_web_sm')
	else:
		raise('Language not supported')
	
	# CREATE CLASSIFIERS
	classes = ['fact','claim','decision','law']
	for c in classes:
		create_classifier(c, nlp)
	sys.exit()

	n_c = int(sys.argv[2])
	text_to_analyse = sys.argv[2]
	

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
		if res_facts:
			facts.append([sentence,res_facts])
		res_claim = classifier_claim.belongs_to_class(sentence)
		if res_claim:
			claims.append([sentence,res_claim])
		res_decisions = classifier_decision.belongs_to_class(sentence)
		if res_decisions:
			decisions.append([sentence,res_decisions])
		res_laws = classifier_laws.belongs_to_class(sentence)
		if res_laws:
			laws.append([sentence,res_laws])
		if not res_laws and not res_decisions and not res_claim and not res_facts:
			arguments.append(sentence)
	
	typical_arguments = closest_n_texts(arguments, n_c=n_c)
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
	print(dic_aux)