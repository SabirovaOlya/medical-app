from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField

from apps.users.models import Doctor, DoctorCategory


class DoctorModelSerializer(ModelSerializer):
    category = StringRelatedField()

    class Meta:
        model = Doctor
        fields = ['user', 'name', 'category']


class DoctorUpdateDeleteModelSerializer(ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=DoctorCategory.objects.all())

    class Meta:
        model = Doctor
        fields = ['name', 'category', 'description', 'score', 'price', 'image', 'hospital']
        read_only_fields = ['id', 'user']
