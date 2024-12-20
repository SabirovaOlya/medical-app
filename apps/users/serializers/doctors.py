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


class DoctorModelForCategorySerializer(ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'description', 'score', 'price', 'image']


class DoctorCategoryModelSerializer(ModelSerializer):
    doctors = DoctorModelForCategorySerializer(many=True, read_only=True, source='doctor_set')

    class Meta:
        model = DoctorCategory
        fields = ['id', 'name', 'doctors']
