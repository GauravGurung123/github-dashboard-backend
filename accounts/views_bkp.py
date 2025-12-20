from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .authentication import CookieTokenAuthentication
from .models import UserProfile
from.serializers import UserCreateRequestsSerializer
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from accounts import services

# Create your views here.
@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def hello_world(request):
    return Response({"message": "hello world"}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    # queryset = UserProfile.objects.filter(deleted_at__isnull=True)
    queryset = UserProfile.active.all()
    serializer_class = UserCreateRequestsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()  # instance here is UserProfile, so no need for .userprofile
        instance.save()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    return services.login_view_handler(request)

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return services.logout_view_handler(request)

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def auth_check_view(request):
    return services.auth_check_view_handler(request)

@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_login(request):
    return services.github_login_handler(request)


@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_callback(request):
    return services.github_callback_handler(request)

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_repos(request):
    return services.github_repos_handler(request)

