from django.urls import path
from . import views

urlpatterns = [
    path("login/github/", views.github_login, name="github-login"),
    path(
        "login/github/callback/",
        views.github_login_callback,
        name="github-login-callback",
    ),
    path("me/", views.get_authenticated_user, name="get-authenticated-user"),
    path("logout/", views.user_logout, name="user-logout"),
]
