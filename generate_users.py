import os
import requests
import csv
import random
import time

token = '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'
headers = {
    'Authorization': 'Bearer ' + token,
    'Accept': 'application/vnd.github+json'
}

def fetch_data(url, params=None):
    global headers

    while True:
        response = requests.get(url, headers=headers, params=params)
        print('REMAINING RESPONSE:', int(response.headers.get('X-RateLimit-Remaining', 0)))
        
        if response.status_code != 200:
            print('ERROR RESPONSE CODE: ', response.status_code, 'RESPONSE:', response.json())

            remaining_rate_limit = int(response.headers.get('X-RateLimit-Remaining', 0))
            rate_limit_reset_time = int(response.headers.get('X-RateLimit-Reset', time.time()))

            if remaining_rate_limit <= 1:
                sleep_time = rate_limit_reset_time - time.time() + 5  # Adding 5 seconds buffer
                print(f"Rate limit exceeded, waiting for {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                time.sleep(60)  # Sleep for 60 seconds
            continue

        return response


repo = ['pytorch', 'opencv', 'flutter', 'tensorflow', 'upscayl', 'rustdesk', 'casbin', 'matplotlib', 'django']


def fetch_merged_prs():
    print('############# FETCHING PR RAISING USERS ############')
    params = {
        'state': 'closed',
        'per_page': 100,
        'page': 1
    }

    idx = 0
    cnt = set()
    merged_users = set()
    rejected_users = set()

    while len(merged_users) <= 1000 and idx < len(repo):
        print('TOTAL:', len(merged_users), 'CNT:', len(cnt), 'PAGE:', params['page'])
        
        url = f'https://api.github.com/repos/{repo[idx]}/{repo[idx]}/pulls'
        response = fetch_data(url, params=params)
        data = response.json()

        if not data or not isinstance(data, list) or len(cnt) >= 150 or params['page'] > 30:
            print('****** FINISHED: ', repo[idx], '*******')
            idx += 1
            cnt = set()
            params['page'] = 1

        for pr in data:
            if 'user' not in pr or 'login' not in pr['user']:
                continue

            if pr['merged_at'] is not None:
                merged_users.add(pr['user']['login'])
                cnt.add(pr['user']['login'])
            else:
                rejected_users.add(pr['user']['login'])
        params['page'] += 1

    return merged_users, rejected_users

def fetch_contributors():
    print('############# FETCHING CONTRIBUTORS ############')
    params = {
        'per_page': 100,
        'page': 1
    }

    contributors = set()
    idx = 0
    cnt = set()
    while len(contributors) < 800 and idx < len(repo):
        print('TOTAL:', len(contributors), 'CNT:', len(cnt), 'PAGE:', params['page'])

        url = f'https://api.github.com/repos/{repo[idx]}/{repo[idx]}/contributors'
        response = fetch_data(url, params=params)
        data = response.json()

        if not data or not isinstance(data, list) or len(cnt) >= 70:
            print('FINISHED FETCHING CONTRIBUTORD FOR:', repo[idx])
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
contributors = fetch_contributors()
inactive_users = random.sample(
    list(rejected_users) + list(contributors - active_users), len(active_users))
inactive_users = set(inactive_users) - active_users

print('active_users:', len(active_users))
print('rejected_users:', len(rejected_users))
print('inactive_user:', len(inactive_users))
print('contributors:', len(contributors))

with open('user_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['user', 'status']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    for iu in inactive_users:
        writer.writerow([iu, 0])

    for au in active_users:
        writer.writerow([au, 1])
