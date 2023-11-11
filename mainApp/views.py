from django.shortcuts import render
import requests
# Create your views here.
from github import Github
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .forms import RepositoryForm


from .utils import fetch_user_repositories
from .utils import fetch_commit_frequency
from .utils import fetch_repository_details
from .utils import fetch_pull_request_trends
from .utils import fetch_issue_data
from .utils import calculate_issue_resolution_time
from .utils import fetch_contributor_activity
# Create your views here.



def github_auth(request):
    # Redirect users to GitHub for authorization
    # github_oauth_url = f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_REDIRECT_URI}"
    # context = {
    #     'github_client_id': settings.GITHUB_CLIENT_ID,
    #     'github_redirect_uri': settings.GITHUB_REDIRECT_URI,
    # }
    return redirect(f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_REDIRECT_URI}")


def github_callback(request):

    # Handle the GitHub callback, exchange the code for an access token
    code = request.GET.get('code')
    print("code")
    print(code)
    settings.GITHUB_CODE = code
    state = request.GET.get('state')
    print("state")
    print(state)

    # Ensure that the state matches for security
    if state != 'YOUR_RANDOM_STATE':
        return HttpResponse("Invalid state. Possible CSRF attack!")

    # Make a POST request to exchange the code for an access token
    # Handle the access token and make API requests here

    return HttpResponse("GitHub OAuth Callback")


# @login_required
def home(request):
    return render(request, 'home.html')

def get_access_token(request):
    print("Im getting access token")
    # The code parameter received from GitHub
    code = request.GET.get('code')
    settings.GITHUB_CODE = code

    # Make a POST request to exchange the code for an access token
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
    }

    response = requests.post('https://github.com/login/oauth/access_token', data=data)
  
    # Handle the response, parse the access token, and store it securely on the server
    if response.status_code == 200:
        access_token = response.text.split('&')[0].split('=')[1]

        print("This is your actual access token:")
        print(access_token)
        settings.GITHUB_ACCESS_TOKEN = access_token
        
        # Store the access token securely on the server
    return render(request,"options.html")
    
   


def select_repository(request):
    access_token = settings.GITHUB_ACCESS_TOKEN
    
    print("in function select repo")
    print(access_token)
    if access_token:
        repositories = fetch_user_repositories(access_token)
        if repositories:
            form = RepositoryForm(initial={'repositories': repositories[0]})  # Pre-fill the form with the first repository
        else:
            form = RepositoryForm()
    else:
        return redirect('github_auth')  # Redirect to GitHub authorization if access token is not available

    return render(request, 'select_repository.html', {'repositories': repositories})



def repository_details(request, owner, repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    print("I'M HERE DO YOU SEE ME?")
    if access_token:
        contributors_data = fetch_contributor_activity(access_token, owner, repo)
        
         # Convert datetime objects to strings
        # contributor_data = {
        #     'login': [str(item['login']) for item in contributor_activity_data],
        #     'activity': [item['activity'] for item in contributor_activity_data],
        # }
        repo_data = fetch_repository_details(access_token, owner, repo)
        commits_data = fetch_commit_frequency(access_token, owner, repo)
        print(commits_data)
        pull_request_trends = fetch_pull_request_trends(access_token, owner, repo)
        issue_data = fetch_issue_data(access_token, owner, repo)
       
        #  or commit_frequency or pull_request_trends or issue_data

        if contributors_data or repo_data or commits_data:
            return render(request, 'repository_details.html', {"commits_data":commits_data,"repo_data":repo_data,'contributors_data': contributors_data,"pull_request_trends":pull_request_trends,"issue_data":issue_data})
        else:
            return render(request, 'error.html', {'message': 'Repository details not found'})
    else:
        return redirect('github_auth')  # Redirect to GitHub authorization if access token is not available

def search_repository(request):
    
    return render(request, 'search_repositories.html')



def options(request):
    return render(request, 'options.html')

def test(request):
    return render(request,'test.html')


from django.http import JsonResponse


from django.http import JsonResponse

def contributor_activity(request, owner, repo):
    access_token = settings.GITHUB_ACCESS_TOKEN  # Replace with the actual access token

    # Fetch real contributor activity data
    
    contributor_activity_data = fetch_contributor_activity(access_token, owner, repo)

    # Convert datetime objects to strings
    contributor_activity_data_json = {
        'labels': [str(item['date']) for item in contributor_activity_data],
        'data': [item['contributions'] for item in contributor_activity_data],
    }

    # Pass the data to the template
    return JsonResponse({'contributor_activity_data_json': contributor_activity_data_json})

def sign_out(request):
    # Clear the stored access token
    settings.GITHUB_ACCESS_TOKEN = None

    # Redirect to the home page or any landing page
    return redirect('home')


def dashboard(request,owner,repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    print("I'M HERE DO YOU SEE ME?")
    if access_token:
        
         # Convert datetime objects to strings
        # contributor_data = {
        #     'login': [str(item['login']) for item in contributor_activity_data],
        #     'activity': [item['activity'] for item in contributor_activity_data],
        # }
        repo_data = fetch_repository_details(access_token, owner, repo)
      

      
        issue_data = fetch_issue_data(access_token, owner, repo)
       
        #  or commit_frequency or pull_request_trends or issue_data

        if repo_data:
            return render(request, 'dashboard.html', {"repo_data":repo_data})
        else:
            return render(request, 'error.html', {'message': 'Repository details not found'})
    else:
        return redirect('github_auth')  # Redirect to GitHub authorization if access token is not available

from urllib.parse import unquote

def recent_commits(request,owner,repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    commits_data = fetch_commit_frequency(access_token, owner, repo)
    return render(request, 'recent_commits.html', {'commits_data': commits_data,'access_token':access_token})
 

def pull_requests(request,owner,repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    pull_request_trends = fetch_pull_request_trends(access_token, owner, repo)
    print("access token that is being passed to pull:")
    print(access_token)
    return render(request, 'pull_requests.html',{'pull_request_trends': pull_request_trends,'access_token': access_token})

def contributors(request,owner,repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    # contributors_data = fetch_contributor_activity(access_token, owner, repo)
    # print("contributors data")
    # print(contributors_data)
    return render(request, 'contributors.html',{'access_token':access_token})

def issue_resolution(request,owner,repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    issue_data = fetch_issue_data(access_token, owner, repo)
    print("access token that is being passed to issue_resolution:")
    print(access_token)
    return render(request, 'issue_resolution.html',{'issue_data': issue_data,'access_token':access_token})


def insights(request,owner,repo):
    access_token = settings.GITHUB_ACCESS_TOKEN
    
    return render(request, 'insights.html',{'access_token':access_token,'owner':owner, 'repo':repo})
    