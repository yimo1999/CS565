import requests
import collections
import csv
import os


def profile_collector(username):
    """
    :param
    username: str
        user's username
    :return:
        None
    """

    # Set the API endpoint URL
    url = "https://api.github.com/users/{username}"
    # Replace {username} with the GitHub username of the user you want to fetch
    # Set the headers with your authentication token
    headers = {
        "Authorization": "Your github authorization code"
    }

    # Make the API request

    response = requests.get(url.format(username=username), headers=headers)
    res = ''
    data_dict = collections.defaultdict()
    data_dict['username'] = username
    data_dict['id'] = response.json()['id']

    # Check if the request was successful
    if response.status_code == 200:
        # Print the user's profile information
        res = response.json()
        # print(res)
    else:
        # Print the error message
        # print("Error fetching user profile information:", response.text)
        return "Error fetching user profile information:", response.text

    # 'followers_url'
    response = requests.get(res['followers_url'])
    followers_num = len(response.json())
    data_dict['followers_num'] = followers_num
    # print('follower num: ', followers_num)

    # 'repos_url'
    response = requests.get(res['repos_url'])
    repos_num = len(response.json())
    data_dict['repos_num'] = repos_num

    # data about star num, watcher num, fork num
    data = data_sum(response.json())
    data_dict['stargazers_sum'] = data[0]
    data_dict['watchers_sum'] = data[1]
    data_dict['forks_sum'] = data[2]

    data_dict['avg_stars_num(per repo)'] = data_dict['stargazers_sum'] // data_dict['repos_num']
    data_dict['avg_watchers_num(per repo)'] = data_dict['watchers_sum'] // data_dict['repos_num']
    data_dict['avg_forks_num(per repo)'] = data_dict['forks_sum'] // data_dict['repos_num']

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
    field_names = ['username', 'id', 'followers_num', 'repos_num',
                   'stargazers_sum', 'watchers_sum', 'forks_sum',
                   'avg_stars_num(per repo)', 'avg_watchers_num(per repo)',
                   'avg_forks_num(per repo)']

    if not os.path.exists('user_profile.csv'):
        with open('user_profile.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerow(data_dict)
    else:
        with open('user_profile.csv', 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            # writer.writeheader()
            writer.writerow(data_dict)

    # print(data_dict)


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

    return [stars_sum, watchers_sum, forks_sum]
