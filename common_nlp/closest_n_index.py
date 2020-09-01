from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.metrics.pairwise import cosine_distances
from collections import Counter
import numpy as np

def closest_n_index(X, n_c=10):
	kmeans = KMeans(n_clusters=n_c, random_state=0).fit(X)
	closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
	return closest, kmeans.labels_
