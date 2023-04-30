import requests
import collections
import csv
import os
import json as j


def event_logger(username):
    print(username)
    # Set the API endpoint URL
    events_url = 'https://api.github.com/users/{username}/events?per_page=100'
    # Replace {username} with the GitHub username of the user you want to fetch
    # Set the headers with your authentication token
    headers = {
        "Authorization": "Your github authorization code"
    }

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
        
    else:
        # Print the error message
        # print("Error fetching user profile information:", response.text)
        return "Error fetching user profile information:", response.text
    




def dict_to_csv(data_dict):
    """
    This function is used to convert the python dictionary
     to a csv format file
    :param
    data_dict: dictionary

    :return:
    None. It will generate a csv format file.
    """
    if not os.path.exists('user_events.csv'):
        with open('user_events.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
            writer.writeheader()
            writer.writerow(data_dict)
    else:
        with open('user_events.csv', 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
            writer.writerow(data_dict)
