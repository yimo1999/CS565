from UserEvents import event_logger
from helper import *

def generate_feature_vector(username):
    vector = []

    # features : # of stars, # of personal repo, # of forked repo, # of accepted PR, # of total PR, [how active?]
    # features : # of personal repo, [how active?]

    forks, stars, count = get_forked_and_stargazed(username)
    accepted, total = get_accepted_and_total_pull_requests(username)
    
    vector.extend([forks, stars, count, accepted, total])
    
    return vector

if __name__ == '__main__':
    print(generate_feature_vector('yihui'))

    