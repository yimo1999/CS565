import requests
import collections
import csv
import os


def repo_info_scrapper():
    # Set the API endpoint URL
    url = "https://api.github.com/repos/pytorch/pytorch"
    # Replace {username} with the GitHub username of the user you want to fetch
    # Set the headers with your authentication token
    headers = {
        "Authorization": "Your github authorization code"
    }

    # Make the API request

    response = requests.get(url, headers=headers)
    res = ''
    data_dict = collections.defaultdict()

    # Check if the request was successful
    if response.status_code == 200:
        # Print the user's profile information
        res = response.json()
        # print(res)
    else:
        # Print the error message
        # print("Error fetching user profile information:", response.text)
        return "Error fetching user profile information:", response.text
    
    data_dict['name'] = res['name']
    data_dict['full_name'] = res['full_name']
    data_dict['private'] = res['private']
    data_dict['owner'] = res['owner']['login']
    data_dict['description'] = res['description']
    data_dict['contributors_url'] = len(requests.get(res['contributors_url']).json()) 
    data_dict['pulls_url'] = len(requests.get('https://api.github.com/repos/pytorch/pytorch/pulls').json()) 
    data_dict['created_at'] = res['created_at']
    data_dict['contributors'] = requests.get(res['contributors_url']).json()

    # print(data_dict)
    dict_to_csv(data_dict)


def dict_to_csv(data_dict):
    """
    This function is used to convert the python dictionary
     to a csv format file
    :param
    data_dict: dictionary

    :return:
    None. It will generate a csv format file.
    """
    if not os.path.exists('repo_info.csv'):
        with open('repo_info.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
            writer.writeheader()
            writer.writerow(data_dict)
    else:
        with open('repo_info.csv', 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_dict.keys())
            writer.writerow(data_dict)