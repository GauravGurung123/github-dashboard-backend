from django.urls import path
from . import views, api_views

# urlpatterns = [
#     path("login/github/", views.github_login, name="github-login"),
#     path(
#         "login/github/callback/",
#         views.github_login_callback,
#         name="github-login-callback",
#     ),
#     path("me/", views.get_authenticated_user, name="get-authenticated-user"),
#     path("logout/", views.user_logout, name="user-logout"),
# ]

urlpatterns = [
    # Web Views
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),

    # API Endpoints
    path('api/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', api_views.LogoutAPIView.as_view(), name='api_logout'),
    path('api/profile/', api_views.UserProfileAPIView.as_view(), name='api_profile'),
    path('api/me/', api_views.CurrentUserAPIView.as_view(), name='api_current_user'),
]