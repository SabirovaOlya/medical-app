from rest_framework.serializers import ModelSerializer

from apps.users.models import Hospital


class HospitalModelSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'user', 'name']
        read_only_fields = ['id', 'user']


class HospitalUpdateDeleteModelSerializer(ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['name', 'about']
        read_only_fields = ['id', 'user']
