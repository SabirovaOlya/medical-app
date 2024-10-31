from rest_framework.serializers import ModelSerializer

from apps.users.models import Doctor


class DoctorModelSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user', 'name']


class DoctorUpdateDeleteModelSerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'description', 'score', 'price', 'image', 'hospital']
        read_only_fields = ['id', 'user']
