from scipy.spatial import distance
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min, silhouette_score

class kmeans_clustering():

    def __init__(self, df, threshold=0.9):
        self.df = df
        self.threshold = threshold
        self.K = 2
    
    def find_clusters(self, find_closest=False):
        # print('Finding clusters')
        X = self.df.values
        k = self.K
        best_k = 2
        sil_score = -1
        max_iter = 10
        # print('Current silhouette score ',sil_score)
        while sil_score < self.threshold and max_iter and k < (len(X) - 1):
            # print('Attempting clustering with k ',k)
            kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
            sil_score_aux = silhouette_score(X,kmeans.labels_)
            if sil_score_aux > sil_score:
                sil_score = sil_score_aux
                best_k = k
            # print('Finished clustering with silhouette score of ',sil_score)
            max_iter -= 1
            k += 1
        kmeans = KMeans(n_clusters=best_k, random_state=0).fit(X)
        if find_closest:
            closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
        else:
            closest = None
        return (closest, kmeans.labels_)


