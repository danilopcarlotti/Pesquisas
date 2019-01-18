from scipy.spatial import distance as dist
from textNormalization import textNormalization
import numpy as np

class word_histogram_comparison():
	def __init__(self):
		self.scipy_methods = {
		"Euclidean" : dist.euclidean,
		"Manhattan" : dist.cityblock,
		"Chebysev" : dist.chebyshev
		}

	def compare_two_hist(histA, histB, method):
		return method(histA, histB)

	def compare_all_all(texts, method):
		results = {}
		for i in range(len(texts)-1):
			textA = texts[i]
			other_texts = texts[:i] + texts[i+1:]
			results[textA[0]] = self.compare_one_all(textA, other_texts, method)
		return results

	def compare_one_all(textA, texts, method):
		txt_nrm = textNormalization()
		results = {}
		id_A, text_A = textA
		histA = txt_nrm.text_to_hist(text_A)
		for id_t, text_t in texts:
			histogram_A_aux = []
			histogram_T_aux = []
			histogram_t = txt_nrm.text_to_hist(text_t)
			for k,v in histA.items():
				if k in histogram_t:
					histogram_A_aux.append(v)
					histogram_T_aux.append(histogram_t[k])
			results[id_t] = method(histogram_A_aux,histogram_T_aux)
		return results

	def texts_to_mean_hist(self, texts, method):
		aux_hist = Counter()
		final_hist = {}
		txt_nrm = textNormalization()
		for t in texts:
			aux_hist += txt_nrm.text_to_hist(t)
		aux_hist = dict(aux_hist)
		texts_size = len(texts)
		for k,v in aux_hist.items():
			final_hist[k] = v/texts_size
		return final_hist

	def mean_hist_dist_texts(self, texts, method):
		mean_hist = 0
		sd_hist = []
		for i in range(len(texts)-1):
			textA = texts[i]
			other_texts = texts[:i] + texts[i+1:]
			mean_aux = 0
			for j in range(len(other_texts)):
				mean_aux += self.compare_two_hist(textA,other_texts[j],method)
			mean_aux = mean_aux/len(other_texts)
			mean_hist += mean_aux
			sd_hist.append(mean_aux)
		return (mean_hist/len(texts),np.std(sd_hist))
