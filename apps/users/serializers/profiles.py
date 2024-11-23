from rest_framework.serializers import ModelSerializer

from apps.users.models import Profile, User


class ProfileModelSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'user']


class UserSelfInfoSerializer(ModelSerializer):
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'profile']
        read_only_fields = ['id', 'username', 'profile']
