from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import LoginSerializer, SignUpSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(tags=['Sign Up'])
class SignUpAPIView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.create(email=email, username=username, is_active=True)
        user.set_password(password)
        user.save()

        # Generate tokens for the new user
        tokens = get_tokens_for_user(user)

        return Response({
            "message": "User registered successfully",
            "tokens": tokens
        })


@extend_schema(tags=['Login'])
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])

        # Generate tokens for the user
        tokens = get_tokens_for_user(user)

        return Response({
            "message": f"Login successful, welcome {user.username}",
            "tokens": tokens
        })
