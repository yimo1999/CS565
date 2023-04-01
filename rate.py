import requests

# Prompt the user to enter a GitHub username
username = input("Enter a GitHub username: ")

# Define the API endpoints we'll be using
repos_url = f"https://api.github.com/users/{username}/repos"
stars_url = f"https://api.github.com/users/{username}/starred"
contributions_url = f"https://api.github.com/users/{username}/events"

# Retrieve information about the user's repositories
repos_response = requests.get(repos_url)
repos = repos_response.json()

# Calculate the user's repo score
repo_score = len(repos) * 5

# Retrieve information about the user's starred repositories
stars_response = requests.get(stars_url)
stars = stars_response.json()

# Calculate the user's star score
star_score = len(stars) * 3

# Retrieve information about the user's contributions
contributions_response = requests.get(contributions_url)
contributions = contributions_response.json()

# Calculate the user's contribution score
contribution_score = 0
for event in contributions:
    if event["type"] == "PushEvent":
        contribution_score += len(event["payload"]["commits"]) * 2

# Calculate the user's overall score
score = repo_score + star_score + contribution_score

# Print out the user's score
print(f"{username}'s score: {score}")
