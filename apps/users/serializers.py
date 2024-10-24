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
            raise ValidationError('Invalid login credentials.')

        if not user.check_password(password):
            raise ValidationError('Invalid login credentials.')

        return {'email': user.email, 'username': user.username}


class EmailModelSerializer(Serializer):
    email = CharField(max_length=255)


class VerifyEmailSerializer(Serializer):
    email = CharField(max_length=255)
    code = IntegerField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        cache_data = cache.get(email)
        if not cache_data:
            raise ValidationError('Verification code expired.')

        if code != cache_data.get('code'):
            raise ValidationError('Code is incorrect.')

        return attrs


class ResetPasswordSerializer(Serializer):
    email = CharField(max_length=255)
    new_password = CharField(write_only=True)
    confirm_password = CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return attrs

    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.set_password(self.validated_data['new_password'])
        user.save()
