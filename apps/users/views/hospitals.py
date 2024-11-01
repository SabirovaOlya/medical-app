from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models import Hospital
from apps.users.serializers import HospitalUpdateDeleteModelSerializer, HospitalModelSerializer


@extend_schema(tags=['Hospitals List'])
class HospitalListCreateView(ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer


@extend_schema(tags=['Hospital Detail'])
class HospitalRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalUpdateDeleteModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()