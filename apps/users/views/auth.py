from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import LoginSerializer, \
    SignUpSerializer


@extend_schema(tags=['Sign Up'])
class SignUpAPIView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        username = serializer.data['username']
        password = serializer.validated_data['password']

        user = User.objects.create(email=email, username=username, is_active=False)
        user.set_password(password)
        user.save()

        return Response({"message": "Success"})


@extend_schema(tags=['Login'])
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        return Response({"message": f"Login successful, welcome {username}"})
