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

# function found originally in https://stackoverflow.com/questions/39216897/plot-pca-loadings-and-loading-in-biplot-in-sklearn-like-rs-autoplot
def biplot(y, score, coeff, labels=None):
    xs = score[:,0]
    ys = score[:,1]
    n = coeff.shape[0]
    scalex = 1.0/(xs.max() - xs.min())
    scaley = 1.0/(ys.max() - ys.min())
    plt.scatter(xs * scalex,ys * scaley, c = y)
    for i in range(n):
        plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
        if labels is None:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("PC{}".format(1))
    plt.ylabel("PC{}".format(2))
    plt.grid()