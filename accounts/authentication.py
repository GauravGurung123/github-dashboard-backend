from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import  exception_handler
from rest_framework import  status

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("auth_token")

        if not token:
            return None
        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid or Expired token")

        return (token_obj.user, token_obj)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return Response({
            "authenticated": False,

        }, status=status.HTTP_401_UNAUTHORIZED)

    return  response