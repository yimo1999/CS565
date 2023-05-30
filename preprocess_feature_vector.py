import json
import csv
import copy

def main():
    name, X = [], []
    with open('feature_vector_dataset.csv', mode ='r') as file:
        # reading the CSV file
        reader = csv.DictReader(file)
        for row in reader:
            name.append(row['id'])
            X.append(json.loads(row['FV']))

    Y = [0] * len(X)

    for idx, vec in enumerate(X):
        if vec[4] and (vec[3]/vec[4]) > 0.25:
            Y[idx] = 1

    
    for idx, vec in enumerate(X):
        new = vec[:4] + vec[5:]
        X[idx] = new



    with open('preprocessed_feature_vector_dataset.csv', mode='a', newline='') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(['id', 'FV', 'Y'])
    
        print('///Generating Feature Vector///')
        for idx in range(len(X)):
            data = [name[idx], X[idx], Y[idx]]
            writer.writerow(data)
                
                    
    print('///Finished///')






if __name__ == '__main__':
    main()