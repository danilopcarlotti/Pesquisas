import sys, pandas as pd, re, os, gc
from collections import Counter
from recursive_folders import recursive_folders
from pca_plot import pca_plot

sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from cluster_representation_graph import graph_clusters
from pesquisas.common_nlp.clustering_topics_regression_texts import (
    texts_of_interest,
    topics_of_interest,
    cosine_dispersion,
    labels_to_csv,
)
from pesquisas.common_nlp.classifier_texts_tfidf import classifier_texts_tfidf
from pesquisas.common_nlp.vectorizer_texts_tfidf import vectorizer_texts_tfidf
from pesquisas.common_nlp.closest_n_index import closest_n_index
from pesquisas.common_nlp.topicModelling import topicModelling
from pesquisas.common_nlp.words_interest_log_reg import (
    words_interest_log_reg,
    create_clf,
)


def main():
    PATH_FILES = (
        "/home/deathstar/Documents/pesquisas_privado/previdenciario/extração_sentenças"
    )
    rec = recursive_folders()
    paths_csv = [
        i
        for i in rec.find_files(PATH_FILES)
        if i[-3:] == "csv"
        and not i.startswith("beta")
        and not re.search(r"todos_textos|labels_to_csv", i)
    ]
    for csv_path in paths_csv:
        gc.collect()
        print(csv_path)
        # PATH AND TITLE FOR REPORTS. Output path for reports and other files
        title_reports = csv_path.split("/")[-1].split(".")[0]
        path_reports = PATH_FILES + "/" + title_reports + "/"
        # PROCESSING OF TEXTS
        print("Processing texts")
        try:
            vectorizer = vectorizer_texts_tfidf(csv_path, use_pca=False)
            X = vectorizer.X
            # CLUSTERING
            print("Clustering")
            closest, labels = closest_n_index(X, n_c=30)
            texts_of_interest(csv_path, closest, labels, path_reports)
        except Exception as e:
            print(e)
            pass
            # vectorizer = vectorizer_texts_tfidf(csv_path)
            # X = vectorizer.X
            # X_pca = vectorizer.X_pca
            # # CLUSTERING
            # print('Clustering')
            # closest, labels,  = closest_n_index(X_pca,n_c=10, center_distances=True)
            # texts_of_interest(csv_path, closest, labels, path_reports)
        # PLOT CLUSTERS
        print("Plotting clusters")
        graph_clusters(X, closest, labels, path_fig=path_reports)
        pca_plot(
            X,
            labels,
            "Representation of clusters - PCA - 3 components",
            prefix=path_reports,
        )
        # CSV OF LABELS
        print("Labels to csv")
        labels_to_csv(labels, prefix=path_reports)
        # # TOPIC MODELLING
        # print('Topic modelling')
        # topics_of_interest(csv_path, path_reports,title_reports)
        # # COSINE DISTANCE DISPERSION
        # print('Cosine dispersion')
        # cosine_dispersion(X,title_reports,path_reports)
    gc.collect()
    # LOGISTIC REGRESSION
    print("Logistic regression")
    csv_path = PATH_FILES + "/todos_textos.csv"
    df = pd.read_csv(csv_path, usecols=["class"])
    classes_target = Counter(df["class"].tolist())
    print("Processing texts")
    vectorizer = vectorizer_texts_tfidf(csv_path, use_pca=False)
    X = vectorizer.X
    var_names = vectorizer.vectorizer.get_feature_names()
    for target in classes_target:
        path_reports = PATH_FILES + "/" + target + "/"
        print("Processing target class ", target)
        y = []
        for i in vectorizer.y:
            if i == target:
                y.append(1)
            else:
                y.append(0)
        classifier = create_clf(X, y)
        variables_of_interest = words_interest_log_reg(classifier, var_names)
        rows = []
        for beta, word in variables_of_interest:
            rows.append({"beta": beta, "word": word})
        df_target = pd.DataFrame(rows, index=[i for i in range(len(rows))])
        df_target.to_csv(
            path_reports + "betas_regressão_classe_" + target + ".csv", index=False
        )


main()
