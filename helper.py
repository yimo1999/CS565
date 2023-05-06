import requests
import collections
import csv
import os

token = ''
headers = {"Authorization": "token " + token}

def get_forked_and_stargazed(username):
    """
    :param
    username: str
        user's username
    :return:
        None
    """
    global headers

    # Set the API endpoint URL
    url = "https://api.github.com/users/{username}"
    # Replace {username} with the GitHub username of the user you want to fetch
    # Set the headers with your authentication token

    # Make the API request
    response = requests.get(url.format(username=username), headers=headers)

    res = ''

    # Check if the request was successful
    if response.status_code == 200:
        # Print the user's profile information
        res = response.json()
    else:
        # Print the error message
        return "Error fetching user profile information:", response.text

    data_dict = collections.defaultdict()
    data_dict['username'] = username
    data_dict['id'] = res['id']

    # 'repos_url'
    response = requests.get(res['repos_url']+'?per_page=100', headers=headers)
    # print(response.status_code)

    # data about star num, watcher num, fork num
    data = data_sum(response.json())

    stars_sum = data[0]
    forks_sum = data[2]
    total = data[3]

    return (forks_sum, stars_sum, total)

def get_accepted_and_total_pull_requests(username):
    # Set the API endpoint URL
    events_url = 'https://api.github.com/users/{username}/events?per_page=100'
    # Replace {username} with the GitHub username of the user you want to fetch
    # Set the headers with your authentication token
    global headers

    # loggged_events = ['WatchEvent', 'PushEvent', 'PullRequestEvent']
    loggged_events = ['PullRequestEvent']

    # Make the API request
    response = requests.get(events_url.format(username=username), headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        json = response.json()
        
        all_events = []
        
        for event in json:
            if event['type'] in loggged_events:
                data_dict = collections.defaultdict()
                data_dict['username'] = username
                data_dict['repository'] = event['repo']['name']

                data = event['payload']

                data_dict['url'] = data['pull_request']['url']
                    
                if event['type'] == 'PullRequestEvent':
                    data_dict['merged'] = False

                all_events.append(data_dict)

                for event in all_events:
                    if event['url'] == data_dict['url'] and data['pull_request']['merged_at'] != None:
                        event['merged'] = True
                
        # print(all_events)
        # print(j.dumps(all_events, indent=2))

        merged_c = len(list(filter(lambda x: x['merged'], all_events)))
        return (merged_c, len(all_events))
    else:
        # Print the error message
        # print("Error fetching user profile information:", response.text)
        return "Error fetching user profile information:", response.text
    
def data_sum(content):
    """
    This function is used to return the sum of stars number,
    the sum of watchers number and the sum forks number

    :parameter
    content: str
        json format data from get request

    :returns
    res: list[int]
        [sum of stars num, sum of watchers num, sum of forks number]
    """
    stars_sum, watchers_sum, forks_sum = 0, 0, 0
    for i in content:
        stars_sum += i['stargazers_count']
        watchers_sum += i['watchers_count']
        forks_sum += i['forks_count']

    return [stars_sum, watchers_sum, forks_sum, len(content)]
