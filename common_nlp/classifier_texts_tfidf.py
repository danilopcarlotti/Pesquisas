from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error
try:
	from textNormalization import textNormalization
except:
	from common_nlp.textNormalization import textNormalization

#CLASSIFIERS
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingRegressor

import pickle, pandas as pd, numpy as np, re, sys, os, matplotlib.pyplot as plt

class classifier_texts_tfidf():

    def __init__(self, classifier_method, use_pca=True, N=10, max_df=0.3, df_path='texts_manually_classified.csv'):
        self.df = pd.read_csv(df_path)
        self.df = self.df[((self.df['class'] == 'possessória individual') | (self.df['class'] == 'possessória coletiva'))]
        self.vectorizer = TfidfVectorizer(max_df=max_df)
        self.txtN = textNormalization()
        self.create_X_y()
        self.use_pca = use_pca
        if use_pca:
            self.create_X_PCA(N)
        self.create_clf(classifier_method)

    def create_clf(self, classifier_method):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=0)
        self.classifier_parent = classifier_method
        self.classifier_parent.fit(self.X_train, self.y_train)

    def create_X_y(self):
        self.normal_texts = [' '.join(i) for i in self.txtN.normalize_texts(self.df['text'].tolist())]
        self.vectorizer.fit(self.normal_texts)
        self.tfidf = self.vectorizer.transform(self.normal_texts)
        self.X = [np.array(i).astype(np.float) for i in self.tfidf.A]
        self.y = self.df['class'].tolist()
    
    def create_X_PCA(self,N):
        self.pca = PCA(n_components=N, whiten=True)
        self.pca_vectorizer = self.pca.fit(self.X)
        self.X = self.pca_vectorizer.transform(self.X)

    def confusion_matrix_clf(self):
        self.y_pred = self.classifier_parent.predict(self.X_test)
        disp = plot_confusion_matrix(self.classifier_parent,self.X_test, self.y_test)
        print(disp.confusion_matrix)
        plt.show()

    def dump_clf(self,prefix='',titulo=''):
        pickle.dump(self.vectorizer,open(prefix+'vectorizer_%s.pickle' % (titulo,),'wb'))
        pickle.dump(self.classifier_parent,open(prefix+'classifier_parent_clf_%s.pickle' % (titulo,),'wb'))
        if self.use_pca:
            pickle.dump(self.pca_vectorizer,open(prefix+'pca_vectorizer_%s.pickle' % (titulo,),'wb'))
        self.confusion_matrix_clf()

if __name__ == "__main__":
    # clf = classifier_texts_tfidf(df_path=sys.argv[1])
    # clf.dump_clf(prefix=sys.argv[2],titulo=sys.argv[3])


    # # LOGISTIC REGRESSION
    # clf = classifier_texts_tfidf(LogisticRegression(penalty='l1',n_jobs=-1,solver='saga'), df_path='texts_manually_classified_teste.csv')
    # clf.confusion_matrix_clf()
    # print(clf.classifier_parent.score(clf.X_test,clf.y_test))
    # # print(clf.classifier_parent.predict(clf.X))
    # # print(clf.classifier_parent.predict_proba(clf.X))

    # # KNN
    clf1 = classifier_texts_tfidf(KNeighborsClassifier(n_neighbors=10,n_jobs=-1), df_path='texts_manually_classified_teste.csv')
    # clf1.confusion_matrix_clf()
    print(clf1.classifier_parent.score(clf1.X_test,clf1.y_test))
    # # print(clf.classifier_parent.predict(clf.X))
    # # print(clf.classifier_parent.predict_proba(clf.X))

    # # GRADIENT BOOSTING REGRESSOR
    # clf2 = classifier_texts_tfidf(GradientBoostingRegressor(n_estimators=5),df_path='texts_manually_classified_teste.csv')
    # print(clf2.classifier_parent.score(clf2.X_test,clf2.y_test))