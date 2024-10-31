from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
