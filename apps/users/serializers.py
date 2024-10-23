from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer, ModelSerializer, IntegerField

from apps.users.models import User, Profile, Hospital, Pharmacy, Client, Doctor


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileModelSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'user']


class HospitalModelSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'about', 'location']


class PharmacyModelSerializer(ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['id']


class ClientModelSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id']


class DoctorModelSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'about', 'price', 'hospital']


class EmailModelSerializer(Serializer):
    email = CharField(max_length=255)
    username = CharField(max_length=150)
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return attrs


class VerifyEmailSerializer(Serializer):
    email = CharField(max_length=255, default='uzblordsardorboy0705@gmail.com')
    code = IntegerField(default=4444)

    def validate(self, attrs: dict):
        email = attrs.get('email')
        code = attrs.get('code')
        cache_code = cache.get(email)

        print(f"Email: {email}, Code: {code}, Cached Code: {cache_code}")

        if cache_code is None:
            raise ValidationError('No code found for this email.')

        if code != cache_code:
            raise ValidationError('Code is incorrect or expired.')

        return attrs


class LoginSerializer(Serializer):
    email = CharField(max_length=255)
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise ValidationError('Invalid login credentials.')

        if not user.is_active:
            raise ValidationError('Email not verified. Please verify your email.')

        return {'email': user.email, 'username': user.username}
