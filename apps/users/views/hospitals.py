from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from apps.users.models import Hospital
from apps.users.serializers import HospitalUpdateDeleteModelSerializer, HospitalModelSerializer


@extend_schema(tags=['Hospitals List'])
class HospitalListCreateView(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer


@extend_schema(tags=['Hospital Detail'])
class HospitalRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalUpdateDeleteModelSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
