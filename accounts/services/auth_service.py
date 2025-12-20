from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

def login_view_handler(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        response = Response({
            "message": "Login successful.",
            "token": token.key
        }, status=status.HTTP_200_OK)

        response.set_cookie(key='auth_token', value=token.key, httponly=True, samesite='Lax' )
        return response
    else:
        return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


def logout_view_handler(request):
    try:
        request.user.auth_token.delete()
    except Token.DoesNotExist:
        pass
    response = Response({
        "message": "Logged Out Successfully."
    }, status=status.HTTP_200_OK)
    response.delete_cookie('auth_token')
    return response

def auth_check_view_handler(request):
    user = request.user
    profile = getattr(user, 'userprofile', None)
    silewate = "https://media.istockphoto.com/id/1142192548/vector/man-avatar-profile-male-face-silhouette-or-icon-isolated-on-white-background-vector.jpg?s=1024x1024&w=is&k=20&c=ISYAkNv_k8SCN_pHkYWqlWdGSbirhx_yCigo7QC8NAw="
    # pic = getattr()

    return Response({
        "authenticated": True,
        "username": request.user.username,
        "data" : {
            'username': request.user.username,
            'full_name': f"{user.first_name} {user.last_name}",
            "email": user.email,
            "phone_number": getattr(profile, 'phone_number', None),
            "profile_pic": silewate
        }
    })