"""
URL configuration for GithubAnalysisDashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views
from mainApp import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns = [
#     # path('admin/', admin.site.urls),
#    
#    
#     # path('github-auth/complete/github/',views.test, name='test'),
#     path('', views.home, name='home'),
#     path('admin/', admin.site.urls),
#     # path('github/', include('mainApp.urls')),
#     path('auth/', views.github_auth, name='github_auth'),
#     path('callback/', views.github_callback, name='github_callback'),
#     # path('home/', views.home, name='home'),  
#     # path('fetch-repository/', views.fetch_repository, name='fetch_repository'),

#     # New URL for the home page
#     # path('github-auth/complete/github/',views.get_access_token,name="get_access_token"),
   
#     path('repository-details/', views.repository_details, name='repository_details'),


#     path('github-auth/complete/github/',views.fetch_repository,name="fetch_repository"),

#     path('fetch-repository/', views.fetch_repository, name='fetch_repository'),
#     path('repository-details/<str:owner>/<str:repo>/', views.repository_details, name='repository_details'),

# ]

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('github-auth/complete/github/',views.get_access_token,name="get_access_token"),
    path('auth/', views.github_auth, name='github_auth'),
    path('select-repository/', views.select_repository, name='select_repository'),
    path('repository-details/<str:owner>/<str:repo>/', views.repository_details, name='repository_details'),
    path('test/', views.test, name='test'),
    path('options/',views.options,name="options.html"),
    path('search-repositories/', views.search_repository, name='search_repository'),
    path('select-repository/', views.select_repository, name='select_repository'),
    path('repository-details/', views.repository_details, name='repository_details'),
#    path('contributor-activity/', views.contributor_activity, name='contributor_activity'),
    path('contributor-activity/', views.contributor_activity, name='contributor_activity'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('dashboard/<str:owner>/<str:repo>/', views.dashboard, name='dashboard'),
    path('recent_commits/<str:owner>/<str:repo>/',views.recent_commits, name = 'recent_commits'),
    path('pull_requests/<str:owner>/<str:repo>/',views.pull_requests, name = 'pull_requests'),
    path('contributors/<str:owner>/<str:repo>/',views.contributors, name = 'contributors'),
    path('issue_resolution/<str:owner>/<str:repo>/',views.issue_resolution, name = 'issue_resolution'),
    path('insights/<str:owner>/<str:repo>/',views.insights, name = 'insights'),

   
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Update your urls.py
