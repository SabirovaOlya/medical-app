from rest_framework.serializers import ModelSerializer

from apps.users.models import Pharmacy


class PharmacyModelSerializer(ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['id', 'user', 'name']
        read_only_fields = ['id', 'user']


class PharmacyUpdateDeleteModelSerializer(ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['name', 'about', 'location']
        read_only_fields = ['id', 'user']
