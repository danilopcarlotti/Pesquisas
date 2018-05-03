from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy


class mNB_classification_text():
	"""Class to help classify texts with scikit"""
	def __init__(self,dados):
		self.dados = dados
		self.count_vectorizer = CountVectorizer()
		self.dataframe = self.dataframe_data(self.dados)
		self.classifier = self.mNB_classifier()

	def dataframe_data(self,data):
		rows = []
		index = []
		index_counter = 1
		for text, class_text in list(data):
			rows.append({'text': text, 'class': class_text})
			index.append(index_counter)
			index_counter += 1
		data_frame = pd.DataFrame(rows, index=index)
		return data_frame

	def training_data(self):
		data = self.dataframe_data(self.dados)
		data = data.reindex(numpy.random.permutation(data.index))
		return data

	def count_words(self):
		counts = self.count_vectorizer.fit_transform(self.dataframe['text'].values)
		return counts

	def mNB_classifier(self):
		counts = self.count_words()
		classifier = MultinomialNB()
		targets = self.dataframe['class'].values
		classifier = classifier.fit(counts, targets)
		return classifier

	def test_mNB(self,test_data):
		example_counts = self.count_vectorizer.transform(test_data)
		predictions = self.classifier.predict(example_counts)
		return predictions

if __name__ == '__main__':
	dados = [('s ssss','s'),('bbb bb','b'),('bbb bb','b'),('sss ss','s'),('sssss ssssssss','s')]
	examples = [('s s','s'),('bbb','b')]
	sck = mNB_classification_text(dados)
	for e, class_e in examples:
		print(e,sck.test_mNB([e]),(sck.test_mNB([e]) == class_e))