from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.metrics.pairwise import cosine_distances
from collections import Counter
import numpy as np, sys, matplotlib.pyplot as plt, pickle


def graph_clusters(X, closest, labels, path_fig=""):
    dicionario_closest = {}
    for c in closest:
        dicionario_closest[labels[c]] = X[c]
    dicionario_distancias = {}
    for i in range(len(labels)):
        try:
            if labels[i] not in dicionario_distancias:
                dicionario_distancias[labels[i]] = []
            distancia_centro = cosine_distances([X[i]], [dicionario_closest[labels[i]]])
            if distancia_centro:
                dicionario_distancias[labels[i]].append(distancia_centro)
        except:
            pass
    dicionario_distancias_medias = {}
    for k, v in dicionario_distancias.items():
        dicionario_distancias_medias[k] = np.mean(v)
    # trocar por bar plot dos clusters

    labels, distance_means = [], []
    for label, distance_m in [
        (label, mean_distance_cluster)
        for label, mean_distance_cluster in dicionario_distancias_medias.items()
    ]:
        labels.append(label)
        distance_means.append(distance_m)
    plt.bar(labels, distance_means)
    plt.title("Density of clusters")
    plt.xlabel("Cluster number")
    plt.ylabel("Mean distance of elements in clusters")
    plt.savefig(path_fig + "Density of clusters.png")
    plt.clf()
    plt.close()
    # plotar um círculo para cada. Centro em (1,1), raio do tamanho médio da distância e limites em (2,2)
    # max_distance = 0
    # for label,mean_distance_cluster in dicionario_distancias_medias.items():
    #     if mean_distance_cluster > max_distance:
    #         max_distance = mean_distance_cluster
    # for label,mean_distance_cluster in dicionario_distancias_medias.items():
    #     fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
    #     circle = plt.Circle((2*max_distance, 2*max_distance), mean_distance_cluster, clip_on=False)
    #     ax.set_xlim((0, 4*max_distance))
    #     ax.set_ylim((0, 4*max_distance))
    #     ax.add_artist(circle)
    #     plt.title('Density cluster %s' % (label,))
    #     fig.savefig(path_fig+'Density cluster %s.png' % (label,))
    #     plt.clf()
    #     plt.close()

    # plotar matriz da distância dos centros uns para os outros
    distancias_centros_clusters = cosine_distances(
        [v for _, v in dicionario_closest.items()],
        [v for _, v in dicionario_closest.items()],
    )

    distancias_centros_clusters_upper_t = np.triu(distancias_centros_clusters)
    plt.matshow(distancias_centros_clusters_upper_t)
    # plt.matshow(distancias_centros_clusters)

    plt.colorbar()
    plt.title("Mutual distance of clusters\n")
    plt.savefig(path_fig + "mutual distance of clusters UT.png")
    plt.clf()
    plt.close()

    pickle.dump(
        distancias_centros_clusters,
        open(path_fig + "mutual distance of clusters.pickle", "wb"),
    )
