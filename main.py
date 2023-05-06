from helper import *
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json

def generate_feature_vector(username):
    vector = []

    # features : # of stars, # of personal repo, # of forked repo, # of accepted PR, # of total PR, [how active?]
    # features : # of personal repo, [how active?]
    # print(get_forked_and_stargazed(username))
    forks, stars, count = get_forked_and_stargazed(username)
    accepted, total = get_accepted_and_total_pull_requests(username)
    activity = contributions_past_year(username)
    
    vector.extend([forks, stars, count, accepted, total, activity])
    
    return vector

def main():
    # all_users = []
    # Y = []
    # with open('users.csv', mode ='r') as file:
    #     # reading the CSV file
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         all_users.append(row['user'])
    #         Y.append(row['status'])

    # X = []
    
    # print('///Generating Feature Vector///')
    # for user in all_users:
    #     print(user)
    #     X.append(generate_feature_vector(user))
    # print('///Finished///')

    # with open('generated_feature_vector.csv', mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['FV', 'Y'])
    #     for x, y in zip(X, Y):
    #         writer.writerow([x, y])

    X, Y = [], []
    with open('generated_feature_vector.csv', mode ='r') as file:
        # reading the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            X.append(json.loads(row['FV']))
            Y.append(int(row['Y']))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.21, random_state=0, shuffle=True)

    nb = GaussianNB(var_smoothing=0.2)
    nb.fit(X_train, y_train)

    y_pred = nb.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1-score:", f1_score(y_test, y_pred))


if __name__ == '__main__':
    main()
