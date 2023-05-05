import os
import requests
import csv
import random
import time

token = ''
headers = {
    'Authorization': 'token ' + token,
    'Accept': 'application/vnd.github+json'
}

# Fetch merged PRs (active users)


def fetch_data(url, params=None):
    while True:
        response = requests.get(url, headers=headers, params=params)
        remaining_rate_limit = int(
            response.headers.get('X-RateLimit-Remaining', 0))
        rate_limit_reset_time = int(
            response.headers.get('X-RateLimit-Reset', time.time()))

        if response.status_code != 200:
            print("Error fetching data:", response.status_code, response.text)
            if remaining_rate_limit <= 1:
                sleep_time = rate_limit_reset_time - time.time() + 5  # Adding 5 seconds buffer
                print(
                    f"Rate limit exceeded, waiting for {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                time.sleep(60)  # Sleep for 60 seconds
            continue

        return response


repo = ['pytorch', 'opencv', 'flutter', 'tensorflow', 'upscayl']


def fetch_merged_prs():
    # url = 'https://api.github.com/repos/pytorch/pytorch/pulls'
    params = {
        'state': 'closed',
        'per_page': 100,
        'page': 1
    }
    idx = 0
    cnt = set()
    merged_users = set()
    rejected_users = set()
    while len(merged_users) <= 350 and idx < len(repo):
        url = f'https://api.github.com/repos/{repo[idx]}/{repo[idx]}/pulls'
        response = fetch_data(url, params=params)
        data = response.json()
        # print(len(merged_users))
        if not data or not isinstance(data, list) or len(cnt) >= 70 or params['page'] > 16:
            # print('fetch_merged_prs', repo[idx])
            # print('cnt:', len(cnt))
            # print('page:', params['page'])
            idx += 1
            cnt = set()
            params['page'] = 1

        for pr in data:
            if 'user' not in pr or 'login' not in pr['user']:
                continue

            if pr['merged_at'] is not None:
                merged_users.add(pr['user']['login'])
                cnt.add(pr['user']['login'])
                # print('cc_cnt:', cnt)
            else:
                rejected_users.add(pr['user']['login'])
        params['page'] += 1

    return merged_users, rejected_users


# def fetch_rejected_prs():
#     url = 'https://api.github.com/repos/pytorch/pytorch/pulls'
#     params = {
#         'state': 'closed',
#         'per_page': 100,
#         'page': 1
#     }
#
#     rejected_users = set()
#
#     while True:
#         response = fetch_data(url, params=params)
#         data = response.json()
#
#         if not data or not isinstance(data, list):
#             break
#
#         for pr in data:
#             if 'user' not in pr or 'login' not in pr['user']:
#                 continue
#
#             if pr['merged_at'] is None:
#                 rejected_users.add(pr['user']['login'])
#
#         params['page'] += 1
#
#     return rejected_users


def fetch_contributors():
    # url = 'https://api.github.com/repos/pytorch/pytorch/contributors'
    params = {
        'per_page': 100,
        'page': 1
    }

    contributors = set()
    idx = 0
    cnt = set()
    while len(contributors) < 250 and idx < len(repo):
        url = f'https://api.github.com/repos/{repo[idx]}/{repo[idx]}/contributors'
        response = fetch_data(url, params=params)
        data = response.json()
        # print(data)
        if not data or not isinstance(data, list) or len(cnt) >= 50:
            # print('fetch_contributors', repo[idx])
            idx += 1
            cnt = set()
            params['page'] = 1

        for contributor in data:
            if 'login' not in contributor:
                continue

            contributors.add(contributor['login'])
            cnt.add(contributor['login'])
        params['page'] += 1

    return contributors


active_users, rejected_users = fetch_merged_prs()
# rejected_users = fetch_rejected_prs()
contributors = fetch_contributors()
inactive_users = random.sample(
    list(rejected_users) + list(contributors - active_users), len(active_users))
inactive_users = set(inactive_users) - active_users
# print('inactive_user:', len(inactive_users))
# print('contributors:', len(contributors))
# print('active_users:', len(active_users))
# print('rejected_users:', len(rejected_users))

with open('user_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['user', 'status']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for iu in inactive_users:
        # print(type(iu))
        # print(iu)
        writer.writerow([iu, 0])

    for au in active_users:
        writer.writerow([au, 1])

