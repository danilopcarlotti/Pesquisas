from sklearn.linear_model import LogisticRegression
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split

def create_clf(X, y):
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=0)
    classifier = LogisticRegression(penalty='l1',n_jobs=-1,solver='saga')
    classifier.fit(X_train, y_train)
    return classifier

def words_interest_log_reg(classifier,var_names):
    variables_of_interest = []
    for beta in range(len(classifier.coef_[0])):
        if classifier.coef_[0][beta]:
            variables_of_interest.append((classifier.coef_[0][beta],var_names[beta]))
    variables_of_interest.sort()
    return variables_of_interest


