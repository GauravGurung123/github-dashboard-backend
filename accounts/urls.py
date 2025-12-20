from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import hello_world, UserViewSet, login_view, logout_view, auth_check_view, github_login, github_callback, github_repos
from accounts import views


router = DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns =[
    path('auth-hello', views.hello_world, name='hello_world'),
    path('', include(router.urls)),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('me', views.auth_check_view, name="auth_check_view_me"),

    path('auth-check', views.auth_check_view, name="auth_check_view"),

    path('github/login', views.github_login, name="github_login"),
    path('github/callback/', views.github_callback, name="github_callback"),
    path("github/profiles", views.github_profiles, name="github_profiles"),
    path("github/profile/unlink/<int:pk>/<str:username>", views.github_profile_unlink, name="github_profile_unlink"),
    path('github/repos/<int:req_id>', views.github_repos, name="github_repos"),
    path('github/repos/events/<int:account_id>', views.github_repo_events, name="github_repo_events"),
    path('github/repos/basic-api/<int:account_id>', views.github_basic_api, name="github_basic_api"),
]
