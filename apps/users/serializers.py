from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import Serializer, ModelSerializer

from apps.users.models import User, Profile, Hospital, Pharmacy, Client, Doctor


class UserModelSerializer(Serializer):
    class Meta:
        model = User.objects.all()
        fields = ['id', 'username']


class ProfileModelSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'user']

    def create(self, validated_data):
        user = validated_data['user']
        role = validated_data['role']

        profile = Profile.objects.create(user=user, role=role)

        if role == Profile.Type.DOCTOR:
            Doctor.objects.create(user=profile)
        elif role == Profile.Type.PHARMACY:
            Pharmacy.objects.create(user=profile)
        elif role == Profile.Type.HOSPITAL:
            Hospital.objects.create(user=profile)
        elif role == Profile.Type.CLIENT:
            Client.objects.create(user=profile, name=user.username)

        return profile


class HospitalModelSerializer(Serializer):
    class Meta:
        model = Hospital
        fields = ['id']


class PharmacyModelSerializer(Serializer):
    class Meta:
        model = Pharmacy
        fields = ['id']


class ClientModelSerializer(Serializer):
    class Meta:
        model = Client
        fields = ['id']


class DoctorModelSerializer(Serializer):
    class Meta:
        model = Doctor
        fields = ['id']


class EmailModelSerializer(Serializer):
    email = CharField(max_length=255)
    username = CharField(max_length=150)

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
        if code != cache_code.get('code'):
            raise ValidationError('Code is incorrect')
        if code != cache_code:
            raise ValidationError('Code expired')
        return attrs
