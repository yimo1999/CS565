from helper import *

def generate_feature_vector(username):
    vector = []

    # features : # of stars, # of personal repo, # of forked repo, # of accepted PR, # of total PR, [how active?]
    forks, stars, count = get_forked_and_stargazed(username)
    accepted, total = get_accepted_and_total_pull_requests(username)
    activity, contributions = contributions_past_year(username)
    
    vector.extend([forks, stars, count, accepted, total, activity, contributions])
    
    return vector

def main():
    X = []
    Y = []

    visited = set()

    with open('feature_vector_dataset.csv', mode ='r') as file:
        # reading the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            visited.add(row['id'])


    with open('user_data.csv', mode ='r') as file:
        # reading the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            X.append(row['user'])
            Y.append(row['status'])

    with open('feature_vector_dataset.csv', mode='a', newline='') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(['id', 'FV', 'Y'])
    
    print('///Generating Feature Vector///')
    for idx, user in enumerate(X):
        print(user)

        if user not in visited:
            data = [user, generate_feature_vector(user), Y[idx]]
            with open('feature_vector_dataset.csv', mode='a', newline='') as data_file:
                writer = csv.writer(data_file)
                writer.writerow(data)
    print('///Finished///')


if __name__ == '__main__':
    main()

