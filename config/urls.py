# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('social_django.urls', namespace='social')),
    path('api/', include('apps.dashboards.urls')),
]


# core/exceptions.py
class GitHubAPIException(Exception):
    """Custom exception for GitHub API errors"""
    pass


class RepositoryNotFoundException(Exception):
    """Repository not found exception"""
    pass


class ContributorNotFoundException(Exception):
    """Contributor not found exception"""
    pass