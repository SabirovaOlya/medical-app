from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models import Doctor
from apps.users.serializers import DoctorUpdateDeleteModelSerializer, DoctorModelSerializer


@extend_schema(tags=['Doctors List'])
class DoctorListCreateView(ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorModelSerializer


@extend_schema(tags=['Doctor Detail'])
class DoctorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
