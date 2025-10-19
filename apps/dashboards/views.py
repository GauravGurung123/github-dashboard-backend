# apps/dashboards/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from social_django.models import UserSocialAuth
from .serializers import DashboardSerializer, RepositorySerializer, ContributorSerializer
from .services.dashboard_service import DashboardService
from core.repositories.contributor_repository import ContributorRepository
from core.repositories.repo_repository import RepositoryRepository
from core.integrations.github_client import GitHubClient, GitHubAPIAdapter


class UserRepositoriesView(APIView):
    """
    GET /api/repositories/
    Get all repositories for the authenticated user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get GitHub access token from social auth
            social_auth = UserSocialAuth.objects.get(user=request.user, provider='github')
            access_token = social_auth.extra_data.get('access_token')

            # Fetch repositories from GitHub
            github_client = GitHubClient(access_token)
            repos = github_client.get_user_repositories()

            # Adapt and serialize
            adapter = GitHubAPIAdapter()
            adapted_repos = [adapter.adapt_repository(repo) for repo in repos]
            serializer = RepositorySerializer(adapted_repos, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserSocialAuth.DoesNotExist:
            return Response(
                {'error': 'GitHub account not connected'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RepositoryContributorsView(APIView):
    """
    GET /api/repositories/{owner}/{repo}/contributors/
    Get all contributors for a specific repository
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, owner, repo):
        try:
            social_auth = UserSocialAuth.objects.get(user=request.user, provider='github')
            access_token = social_auth.extra_data.get('access_token')

            # Initialize service
            service = DashboardService(access_token)

            # Sync repository data (fetch contributors)
            service.sync_repository_data(owner, repo)

            # Get contributors from MongoDB
            contributor_repo = ContributorRepository()
            contributors = contributor_repo.get_by_repository(f"{owner}/{repo}")

            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ContributorDashboardView(APIView):
    """
    GET /api/dashboard/{owner}/{repo}/{username}/
    Generate and retrieve dashboard for a specific contributor
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, owner, repo, username):
        try:
            social_auth = UserSocialAuth.objects.get(user=request.user, provider='github')
            access_token = social_auth.extra_data.get('access_token')

            # Initialize service
            service = DashboardService(access_token)

            # Generate dashboard
            dashboard = service.generate_contributor_dashboard(owner, repo, username)

            serializer = DashboardSerializer(dashboard)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AllContributorsDashboardView(APIView):
    """
    POST /api/dashboard/{owner}/{repo}/generate-all/
    Generate dashboards for all contributors in a repository
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, owner, repo):
        try:
            social_auth = UserSocialAuth.objects.get(user=request.user, provider='github')
            access_token = social_auth.extra_data.get('access_token')

            # Initialize service
            service = DashboardService(access_token)

            # Generate all dashboards
            dashboards = service.generate_all_contributors_dashboards(owner, repo)

            return Response(
                {
                    'message': f'Generated {len(dashboards)} dashboards',
                    'count': len(dashboards)
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )