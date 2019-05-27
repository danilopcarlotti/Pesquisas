import numpy as np
from sklearn import svm
from sklearn.cluster import DBSCAN


class outlier_detection():
	def __init__(self):
		self.svm_estimator = None

	def dbscan_dados(self, X, epsilon=0.5):
		clustering = DBSCAN(eps=epsilon).fit(X)
		return clustering.labels_

	def outlier_previous_mean(self, X, maxN, interval=2):
		pos_mean = []
		neg_mean = []
		for i in range(0,maxN):
			if i+interval < len(X):
				aux_list = X[i:i+interval]
				for j in range(len(aux_list)-1):
					result = aux_list[j+1] - aux_list[j]
					if result > 0:
						pos_mean.append(result)
					else:
						neg_mean.append(result)
		return (np.mean(pos_mean),np.std(pos_mean),np.mean(neg_mean),np.std(neg_mean))

	def outlier_svm(self, X, Y=[]):
		estimator = svm.OneClassSVM()
		if len(Y):
			estimator.fit(Y)
		else:
			estimator.fit(X[:50])
		return estimator.predict(X)

	def pm_predictor(self, X, maxN,interval=2, stdD=3):
		pos_mean, pos_mean_std, neg_mean, neg_mean_std = self.outlier_previous_mean(X, maxN, interval=interval)
		classes_predictions = []
		class_n = 0
		for i in range(maxN,len(X)-1):
			difference = X[i+1]-X[i]
			if difference > 0:
				if abs(difference - pos_mean) > abs(stdD*pos_mean_std):
					classes_predictions.append(class_n)
					class_n += 1
				else:
					classes_predictions.append(class_n)
			else:
				if abs(difference - neg_mean) > abs(stdD*neg_mean_std):
					classes_predictions.append(class_n)
					class_n += 1
				else:
					classes_predictions.append(class_n)
		classes_predictions.append(class_n)
		return classes_predictions

	def supervised_svm(self, X, y):
		# vetor de dados
		# vetor com as classes de cada tupla de X
		self.svm_estimator = svm.SVC(gamma='scale')
		self.svm_estimator.fit(X, y)

def main():
	o = outlier_detection()
	test = [1,2,0,5,6,1,2,1,1,300,3001,1,2,3]
	print(o.pm_predictor(test,5))


if __name__ == '__main__':
	main()