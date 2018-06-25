from nltk import stem
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from stopwords_pt import stopwords_pt
import numpy, pandas as pd, nltk
# nltk.download('rslp')

class mNB_classification_text():
	"""Class to help classify texts with scikit"""
	def __init__(self,dados):
		self.dados = dados
		self.dataframe = self.dataframe_data()
		self.count_vectorizer = CountVectorizer(analyzer=self.stemmer,stop_words=[line for line in open('stopwords_pt.txt','r')])
		self.word_counts = self.count_words()
		self.targets = self.dataframe['class'].values
		self.classifier = self.mNB_classifier()

	def count_words(self):
		word_counts = self.count_vectorizer.fit_transform(self.dataframe['text'].values)
		return word_counts

	def dataframe_data(self):
		rows = []
		index = []
		index_counter = 1
		for text, class_text in self.dados:
			rows.append({'text': text, 'class': class_text})
			index.append(index_counter)
			index_counter += 1
		data_frame = pd.DataFrame(rows, index=index)
		return data_frame

	def mNB_classifier(self):
		classifier = MultinomialNB()
		classifier = classifier.fit(self.word_counts, self.targets)
		return classifier

	def predict_mNB(self,predict_data, as_dict=False):
		example_word_counts = self.count_vectorizer.transform(predict_data)
		predictions = self.classifier.predict(example_word_counts)
		if as_dict:
			predictions_dict = {}
			for index, prediction in numpy.ndenumerate(predictions):
				predictions_dict[predict_data[index[0]]] = prediction
			return predictions_dict
		else:
			return predictions

	def stemmer(self, words):
		analyzer = CountVectorizer().build_analyzer()
		stemmer = nltk.stem.RSLPStemmer()
		return (stemmer.stem(w) for w in analyzer(words))

	def training_data(self):
		data = self.dataframe_data()
		data = data.reindex(numpy.random.permutation(data.index))
		return data

	def validate_score(self, cv=None):
		mNB = MultinomialNB()
		scores = cross_val_score(mNB, self.word_counts, self.targets, cv=cv)
		return scores

if __name__ == '__main__':
	dados = [('s ssss','s'),('bbb bb','b'),('bbb bb','b'),('sss ss','s'),('sssss ssssssss','s'),('s ssss','s'),('bbb bb','b'),('bbb bb','b'),('sss ss','s'),('sssss ssssssss','s'),('s ssss','s'),('bbb bb','b'),('bbb bb','b'),('sss ss','s'),('sssss ssssssss','s'),('s ssss','s'),('bbb bb','b'),('bbb bb','b'),('sss ss','s'),('sssss ssssssss','s')]
	sck = mNB_classification_text(dados)
	examples = [('s s','s'),('bbb','b')]
	for e, class_e in examples:
		print(e,sck.predict_mNB([e]),(sck.predict_mNB([e]) == class_e))
	examples2 = ['bbb','ss s','bb bb bbb','s s']
	print(sck.predict_mNB(examples2, as_dict=True))
	print(numpy.mean(sck.validate_score(cv=8)))