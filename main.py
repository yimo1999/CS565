from helper import *
import json
import enum
import numpy as np
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, RepeatedStratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns


class MLModel(enum.Enum):
    NaiveBayes = 0
    KNN = 1
    SVM = 2
    DecisionTree = 3
    LogisticRegression = 4

# NB, KNN, SVM(rbf), Decision Tree, Logistic Regression

def get_model(type):
    print('MODEL:', type.name)
    if type == MLModel.NaiveBayes:
        model = GaussianNB(var_smoothing=11e-08)
        
        return model
    elif type == MLModel.KNN:
        model = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

        hyperparameters = {
            'n_neighbors' : [5,7,9,11,13,15],
            'weights' : ['uniform','distance'],
            'metric' : ['minkowski','euclidean','manhattan']
        }

        search = GridSearchCV(model, hyperparameters, cv=cv)
        
        return search
    elif type == MLModel.SVM:
        model = svm.SVC(kernel='rbf')
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

        hyperparameters = {
            'C': [0.1, 1, 10, 100, 1000],
            'gamma': [1, 0.1, 0.01, 0.001, 0.0001],
            'kernel': [ 'rbf', 'sigmoid']
        }

        search = GridSearchCV(model, hyperparameters, cv=cv)
        return search
    elif type == MLModel.DecisionTree:
        model = DecisionTreeClassifier(random_state=123)

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
        
        # DecisionTreeClassifier(criterion='entropy', max_features='sqrt', min_samples_leaf=4, min_samples_split=2, max_depth=3)
        return search
    elif type == MLModel.LogisticRegression:
        model = LogisticRegression(max_iter=100, penalty='l2', tol=0.1, solver='liblinear')

        return model

    return model
    


def main():
    X, Y = [], []

    accuracy, precision, recall, f1 = [], [], [], []

    with open('preprocessed_feature_vector_dataset.csv', mode ='r') as file:
        # reading the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            X.append(json.loads(row['FV']))
            Y.append(int(row['Y']))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=0, shuffle=True)

    for m in range(5):
        m_type = MLModel(value=m)
        model = get_model(type=m_type)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy.append(accuracy_score(y_test, y_pred))
        precision.append(precision_score(y_test, y_pred))
        recall.append(recall_score(y_test, y_pred))
        f1.append(f1_score(y_test, y_pred))

        print("Accuracy:", accuracy[-1])
        print("Precision:", precision[-1])
        print("Recall:", recall[-1])
        print("F1-score:", f1[-1])
        print('')

        # confusion_matrix(y_test, y_pred, m_type)
        # generate_ROC_curve(model, X_test, y_test, m_type)
    # generate_bar_chart(accuracy, precision, recall, f1)


    

    
def confusion_matrix(y_test, y_pred, m_type):
    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Plot confusion matrix
    plt.figure(figsize=(4, 4))
    sns.heatmap(cm, annot=True, cmap="Blues")
    plt.title(f"{m_type.name} Confusion Matrix")
    plt.ylabel("Actual label")
    plt.xlabel("Predicted label")
    plt.show()

    # Show confusion matrix
    plt.show()


def generate_ROC_curve(model, X_test, y_test, m_type):
    # Get predicted probabilities of the test set
    y_prob = model.predict_proba(X_test)[:, 1]

    # Compute ROC curve and ROC AUC score
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = roc_auc_score(y_test, y_prob)

    # Plot ROC curve
    plt.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--', label='Random guess')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.title(f'{m_type.name} Receiver Operating Characteristic Curve')
    plt.legend(loc="lower right")
    plt.show()
    print('\n')

def generate_bar_chart(accuracy, precision, recall, f1_score):
    # Define the data
    model_names = ['NaiveBayes', 'KNN', 'SVM', 'DecisionTree', 'LogisticRegression']

    # Set plot parameters
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    opacity = 0.8
    index = np.arange(len(model_names))

    # Plot bars
    rects1 = ax.bar(index, accuracy, bar_width, alpha=opacity, color='b', label='Accuracy')
    rects2 = ax.bar(index + bar_width, precision, bar_width, alpha=opacity, color='g', label='Precision')
    rects3 = ax.bar(index + 2*bar_width, recall, bar_width, alpha=opacity, color='r', label='Recall')
    rects4 = ax.bar(index + 3*bar_width, f1_score, bar_width, alpha=opacity, color='y', label='F1-score')

    # Add labels to bars
    for i, rect in enumerate(rects1):
        ax.text(rect.get_x() + rect.get_width() / 2.0, 1.02 * rect.get_height(), f'{accuracy[i]:.3f}', ha='center')
    for i, rect in enumerate(rects2):
        ax.text(rect.get_x() + rect.get_width() / 2.0, 1.02 * rect.get_height(), f'{precision[i]:.3f}', ha='center')
    for i, rect in enumerate(rects3):
        ax.text(rect.get_x() + rect.get_width() / 2.0, 1.02 * rect.get_height(), f'{recall[i]:.3f}', ha='center')
    for i, rect in enumerate(rects4):
        ax.text(rect.get_x() + rect.get_width() / 2.0, 1.02 * rect.get_height(), f'{f1_score[i]:.3f}', ha='center')

    # Set axis labels and title
    ax.set_xlabel('Model')
    ax.set_ylabel('Score')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(index + 2*bar_width)
    ax.set_xticklabels(model_names)

    # Add legend and show plot
    ax.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
