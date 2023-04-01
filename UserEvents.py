import requests
import collections
import csv
import json as j


def event_logger(username):
    # Set the API endpoint URL
    events_url = 'https://api.github.com/users/{username}/events'
    # Replace {username} with the GitHub username of the user you want to fetch
    # Set the headers with your authentication token
    headers = {
        "Authorization": "Your github authorization code"
    }

    # Make the API request
    response = requests.get(events_url.format(username=username), headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        json = response.json()
        
        all_events = []
        
        for event in json:
            # print(event)
            if event['type'] == 'WatchEvent' or event['type'] == 'PushEvent' or event['type'] == 'PullRequestEvent':
                data_dict = collections.defaultdict()
                data_dict['username'] = username
                data_dict['id'] = event['id']
                data_dict['user'] = event['actor']
                data_dict['repository'] = event['repo']
                data_dict['created_at'] = event['created_at']
                data_dict['type'] = event['type']

                payload = collections.defaultdict()
                data = event['payload']

                if event['type'] == 'WatchEvent':
                    payload['action'] = data['action']

                elif event['type'] == 'PushEvent':
                    payload['push_id'] = data['push_id']
                    payload['commits'] = data['commits']
                    
                elif event['type'] == 'PullRequestEvent':
                    payload['action'] = data['action']
                    payload['number'] = data['number']
                    payload['pull_request'] = data['pull_request']
                
                data_dict['payload'] = payload

                all_events.append(data_dict)
        # print(all_events)
        # print(j.dumps(all_events, indent=2))
    else:
        # Print the error message
        # print("Error fetching user profile information:", response.text)
        return "Error fetching user profile information:", response.text
