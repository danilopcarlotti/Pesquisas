import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

def pca_plot(X, labels, titulo, prefix=''):
    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(X)
    label_dictionary = {}
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(labels)):
        if labels[i] not in label_dictionary:
            label_dictionary[labels[i]] = []
        label_dictionary[labels[i]].append(principalComponents[i])
    for l,values in label_dictionary.items():
        x = [i[0] for i in values]
        y = [i[1] for i in values]
        z = [i[2] for i in values]
        ax.scatter(x,y,z,label=l)
        ax.legend()
    plt.title(titulo)
    plt.savefig(prefix+titulo+'.png')
    plt.clf()
