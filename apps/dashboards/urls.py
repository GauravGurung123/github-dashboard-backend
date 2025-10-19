# apps/dashboards/urls.py
from django.urls import path
from .views import (
    UserRepositoriesView,
    RepositoryContributorsView,
    ContributorDashboardView,
    AllContributorsDashboardView
)

urlpatterns = [
    path('repositories/', UserRepositoriesView.as_view(), name='user-repositories'),
    path('repositories/<str:owner>/<str:repo>/contributors/',
         RepositoryContributorsView.as_view(), name='repository-contributors'),
    path('dashboard/<str:owner>/<str:repo>/<str:username>/',
         ContributorDashboardView.as_view(), name='contributor-dashboard'),
    path('dashboard/<str:owner>/<str:repo>/generate-all/',
         AllContributorsDashboardView.as_view(), name='generate-all-dashboards'),
]
