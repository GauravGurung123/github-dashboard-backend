from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..authentication import CookieTokenAuthentication
# from ..models import UserProfile, GithubAccount4
from accounts.models import UserProfile, GithubAccount
from ..serializers import UserCreateRequestsSerializer

from django.utils import timezone
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.conf import settings
import requests
from django.shortcuts import redirect

from core_services import debug


def github_login_handler(request):
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        f"&scope=repo,user"
    )
    return Response({"auth_url": github_auth_url})


def github_callback_handler(request):
    code = request.GET.get('code')
    if not code:
        return Response({"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

    # Exchange the code for an access token
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
    )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return Response({"error": "Failed to retrieve access token"}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch the user's GitHub profile
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"}
    )
    user_data = user_response.json()
    github_username = user_data.get("login")

    if not github_username:
        return Response({"error": "Failed to get GitHub user info"}, status=status.HTTP_400_BAD_REQUEST)

    # Save or update the GitHub account
    GithubAccount.objects.update_or_create(
        user=request.user,
        defaults={
            "access_token": access_token,
            "github_username": github_username
        }
    )

    return redirect("http://localhost:5173")



def github_callback_handler_bkp(request):
    code = request.GET.get('code')
    if not code:
        return Response({"error": "Missing code"}, status=status.HTTP_400_BAD_REQUEST)

    token_response = request.post(
        "https://github.com/login/oauth/access_token",
        data = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
    )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        return Response({"error": "Failed to retrieve access token"}, status=status.HTTP_400_BAD_REQUEST)

    github_username = request.get("login")

    GithubAccount.objects.update_or_create(
        user = request.user,
        defaults={
            "access_token": access_token,
            "github_username" : github_username
        }
    )

    return Response({
        "message": "GitHub account linked successfully.",
        "github_username": github_username
    }, status=status.HTTP_200_OK)

def github_linked_profiles_handler(request):
    accounts = request.user.userprofile.active_github_accounts
    if not accounts:
        return Response({"status": False, "message": "GitHub account not linked"})

    accounts_data = [
        {"id": account.id, "username": account.github_username, "linked_at": account.linked_at.strftime("%Y-%m-%d") if account.linked_at else None }
        for account in accounts
    ]
    return Response({"status": True, "data": accounts_data})

def github_repos_handler(request, req_id):
    account = GithubAccount.objects.filter(id=req_id).first()
    url = request.GET.get('url')
    if not url or url.lower() == 'null':
        url = 'https://api.github.com/user/repos?per_page=10&page=1'
    if account.user_id != request.user.id:
        return Response({"status": False, "message": "Unauthorized"})

    token = account.access_token
    response = (requests.get(
        url,
        headers={"Authorization": f"token {token}"}
    ))

    link_header = response.headers.get("Link", "")
    pagination = {}

    # parse <https://api.github.com/user/repos?per_page=10&page=2>; rel="next", <https://api.github.com/user/repos?per_page=10&page=9>; rel="last"
    if link_header:
        links = link_header.split(",")
        for link in links:
            url_part, rel_part = link.split(";")
            url = url_part.strip()[1:-1] # removing <>
            rel = rel_part.strip().split("=")[1].strip('"')
            pagination[rel] = url

    repos = response.json()
    return Response({
        'status': True,
        'repos': repos,
        'pagination': pagination,
    })

def github_basic_api_handler(request, account_id):
    account = GithubAccount.objects.filter(id=account_id).first()
    if not account:
        return Response({
            "status": False,
            "message": "Unauthorized"
        }, status=status.HTTP_401_UNAUTHORIZED)

    url = request.GET.get('url')
    if not url:
        return Response({
            "status": False,
            "message": "url required"
        }, status=status.HTTP_400_BAD_REQUEST)
    token = account.access_token
    response = requests.get(url, headers={"Authorization": f"token {token}"}).json()
    return Response(response)

def github_events_handler(request, account_id):
    # account_id =  request.GET.get('account_id') if not account_id

    repo = request.GET.get('repo')
    if not account_id or not repo:
        return Response({"status": False, "message": "account_id and repo required"})

    account = GithubAccount.objects.filter(id=account_id).first()
    if not account or account.user_id != request.user.id:
        return Response({"status": False, "message": "Unauthorized"})

    url = f'https://api.github.com/repos/{account.github_username}/{repo}/events'
    token = account.access_token
    response = (requests.get(url, headers={"Authorization": f"token {token}"})).json()
    return Response({"status": False, "message": "Unauthorized", 'data': response})

def github_profile_unlink_handler(request, pk, username):
    account = GithubAccount.objects.filter(id=pk, github_username=username, user_id=request.user.id).first()
    if not account :
        return Response({"status": False, "message": "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

    account.soft_delete()
    account.save()

    return Response({"status" : True, "message": "Successfully unlinked"})
