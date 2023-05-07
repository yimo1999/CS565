from helper import *
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
import json
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import enum



class MLModel(enum.Enum):
    NaiveBayes = 1
    KNN = 2
    SVM = 3
    DecisionTree = 4
    LogisticRegression = 5

# NB, KNN, SVM(rbf), Decision Tree, Logistic Regression


def get_model(type):
    print('MODEL:', type.name)
    if type == MLModel.NaiveBayes:
        model = GaussianNB(var_smoothing=0.2)
        return model
    elif type == MLModel.KNN:
        model = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
        return model
    elif type == MLModel.SVM:
        model = svm.SVC(kernel='rbf')
        return model
    elif type == MLModel.DecisionTree:
        model = DecisionTreeClassifier(random_state=42)

        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

        hyperparameters = {
            'max_depth': [3, 5, 7],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2'],
            'criterion': ['gini', 'entropy']
        }

        search = GridSearchCV(model, hyperparameters, cv=cv)
        search = RandomizedSearchCV(model, hyperparameters, cv=5, n_iter=10, random_state=42)
        
        return search
    elif type == MLModel.LogisticRegression:
        model = LogisticRegression()
        return model

    return model
    


def main():
    X, Y = [], []
    with open('feature_vector_dataset.csv', mode ='r') as file:
        # reading the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            X.append(json.loads(row['FV']))
            Y.append(int(row['Y']))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=0, shuffle=True)

    model = get_model(MLModel.SVM)
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1-score:", f1_score(y_test, y_pred))


if __name__ == '__main__':
    main()
