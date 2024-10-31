from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer

from apps.users.models import User


class SignUpSerializer(Serializer):
    email = CharField(max_length=255)
    username = CharField(max_length=150)
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        elif User.objects.filter(username=username).exists():
            raise ValidationError('A user with this username already exists')
        return attrs


class LoginSerializer(Serializer):
    email = CharField(max_length=255)
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('Login or password incorrect')

        if not user.check_password(password):
            raise ValidationError('Login or password incorrect')

        return {'email': user.email, 'username': user.username}
