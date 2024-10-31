from rest_framework.serializers import ModelSerializer

from apps.users.models import Profile


class ProfileModelSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'user']
