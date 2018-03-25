import re, nltk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn.cluster import KMeans
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

class dataAnalysis():
	"""Python class for data analysis and classification"""
	def __init__(self):
		pass

	def tupleFrequency(self,tupleT):
		frequencyDictionary = {}
		for item in tupleT:
			if item in frequencyDictionary.keys():
				frequencyDictionary[item] += 1
			else:
				frequencyDictionary[item] = 1
		return frequencyDictionary

	def plotScatter(self, title, xAxis, yAxis,xLabel,yLabel):
		try:
			plt.plot(xAxis, yAxis, 'ro')
		except:
			y = yAxis
			plt.yticks(y, xAxis)
			plt.plot(yAxis,y,'ro')
			for a,b in zip(yAxis,y):
				plt.annotate(a,xy=(a,b))
		if xAxis:
			plt.xlabel(xAxis)
		if yAxis:
			plt.ylabel(yAxis)
		plt.title(title)
		plt.tight_layout()
		plt.savefig(title+".png", dpi=80)

	def histogramPlot(self,tupleT,title,minimum,maximum,interval,xLabel,yLabel):
		bins = [x for x in range(minimum,maximum,interval)]
		plt.hist(tupleT,bins)
		plt.title(title)
		plt.tight_layout()
		plt.savefig(title+".png", dpi=80)

	def plotarbox(self,tupleT,title):
		plt.boxplot(tupleT)
		plt.title(title)
		plt.tight_layout()
		plt.savefig(title+".png", dpi=80)

	def kMeans(self,k,dataFrame,title,xLabel,yLabel):
		kmeans = KMeans(n_clusters=k)
		kmeans.fit(dataFrame)
		labels = kmeans.predict(dataFrame)
		centroids = kmeans.cluster_centers_
		plt.title(title)
		plt.xlabel(xLabel)
		plt.ylabel(yLabel)
		plt.scatter(dataFrame['x'], dataFrame['y'], alpha=0.5, edgecolor='k')
		for idx, centroid in enumerate(centroids):
			plt.scatter(*centroid)
		plt.savefig(title+".png", dpi=80)

	def plotScatter3D(title,list_x,list_y,list_z,xLabel,yLabel,zLabel,tickerT=1.0):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(np.array(list_x),np.array(list_y),np.array(list_z),zdir='z', s=20, c=None, depthshade=True)
		ax.xaxis.set_major_locator(ticker.MultipleLocator(base=tickerT))
		ax.yaxis.set_major_locator(ticker.MultipleLocator(base=tickerT))
		ax.zaxis.set_major_locator(ticker.MultipleLocator(base=tickerT))
		ax.set_xlabel(xLabel)
		ax.set_ylabel(yLabel)
		ax.set_zlabel(zLabel)
		plt.savefig(title+".png", dpi=80)

	def ngramFreq(self,text,n):
		''' Returns a Counter object with the frequency of each ngram in the text '''
		token = nltk.word_tokenize(text)
		Ngram = ngrams(token,n)
		return Counter(Ngram)

