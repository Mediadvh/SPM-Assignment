import requests
from django.conf import settings




def fetch_user_repositories(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',  # Recommended header
    }
    print("headers")
    print(headers)
    url = 'https://api.github.com/users/mediadvh/repos'
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        
        repositories = response.json()
    
        # Filter the repositories to extract relevant information, e.g., name and owner
        repository_info = [{'name': repo['name'], 'owner': repo['owner']} for repo in repositories]
        return repository_info
    else:
        print("fetching user repo unsuccessfull with access token")
        print(access_token)
        return []  # Return an empty list if there was an issue fetching repositories


def fetch_repository_details(access_token,owner, repo):
    # Retrieve the access token from where you have stored it
    print("access_token")
    print(access_token)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',  # Recommended header
    }

    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("response code is 200 ")
        return response.json()
    elif response.status_code == 301:
        print("response code is 301 ")
        # Handle redirection (if needed)
        return None
    elif response.status_code == 403:
        print("response code is 403 ")
        # Handle Forbidden error
        return None
    elif response.status_code == 404:
        print("response code is 404 ")
        # Handle Resource Not Found error
        return None
    else:
        print("response code is not known ")
        # Handle other errors or return None
        return None





def fetch_commit_frequency(access_token, owner, repo):
    # headers = {
    #     'Authorization': f'{access_token}',
    #     'Accept': 'application/vnd.github+json',
    # }
    # url = f'https://api.github.com/repos/{owner}/{repo}/stats/participation'
    # response = requests.get(url, headers=headers)

    # if response.status_code == 200:
    #     commit_data = response.json()
    #     return commit_data
    # else:
    #     return None  # Handle the case where data could not be fetched
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commit_data = response.json()
        return commit_data
    else:
        return None 



def fetch_pull_request_trends(access_token, owner, repo):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls?state=all'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pull_requests = response.json()
        return pull_requests
    else:
        return None  # Handle the case where data could not be fetched

import requests

def fetch_issue_data(access_token, owner, repo):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issue_data = response.json()
        return issue_data
    else:
        return None  # Handle the case where data could not be fetched

from datetime import datetime



def calculate_issue_resolution_time(issue):
    created_at = datetime.strptime(issue['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    
    # Check if 'closed_at' is not None
    if issue['closed_at']:
        closed_at = datetime.strptime(issue['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
        resolution_time = closed_at - created_at
    else:
        resolution_time = None  # Issue is not closed, resolution time is None
    
    return resolution_time

def fetch_contributor_activity(access_token, owner, repo):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github+json',
    }
    print("headers")
    print(headers)
    # Fetch contributors
    contributors_url = f'https://api.github.com/repos/{owner}/{repo}/contributors'
    contributors_response = requests.get(contributors_url, headers=headers)

    contributor_activity = []

    if contributors_response.status_code == 200:
        contributors = contributors_response.json()

        for contributor in contributors:
            contributor_login = contributor['login']

            # Fetch recent activity for each contributor
            activity_url = f'https://api.github.com/users/{contributor_login}/events/public'
            activity_response = requests.get(activity_url, headers=headers)

            if activity_response.status_code == 200:
                contributor_activity.append({
                    'login': contributor_login,
                    'activity': activity_response.json()
                })
   

    return contributor_activity


from datetime import datetime, timedelta

def is_access_token_valid(access_token):
    # Check if the access token exists and is not expired
    if not access_token:
        return False

    # Fetch the expiration time from the access token
    expiration_time = datetime.utcfromtimestamp(int(access_token['expires_at']))

    # Check if the token is expired or will expire within a certain time frame (e.g., 5 minutes)
    return expiration_time > datetime.utcnow() + timedelta(minutes=5)
