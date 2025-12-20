from rest_framework.permissions import IsAuthenticated
from ..authentication import CookieTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from core_services.exception import handle_exception
from accounts import services

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
def github_repos(request, req_id):
    try: return services.github_repos_handler(request, req_id)
    except Exception as e: return handle_exception(e, context={"request":request})

@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_profiles(request):
    try: return services.github_linked_profiles_handler(request)
    except Exception as e: return handle_exception(e, context={"request":request})

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_basic_api(request, account_id):
    try: return services.github_basic_api_handler(request, account_id)
    except Exception as e: return handle_exception(e, context={"request":request})

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_repo_events(request, account_id):
    try: return services.github_events_handler(request, account_id)
    except Exception as e: return handle_exception(e, context={"request":request})

@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def github_profile_unlink(request, pk, username):
    try: return services.github_profile_unlink_handler(request, pk, username)
    except Exception as e : return handle_exception(e, context={"request":request})