from rest_framework.serializers import ModelSerializer

from apps.users.models import Client


class ClientModelSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'name']
        read_only_fields = ['id', 'user']


class ClientUpdateDeleteModelSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'weight', 'height', 'blood_pressure']
        read_only_fields = ['id', 'user']
