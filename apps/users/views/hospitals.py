from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from apps.users.models import Hospital
from apps.users.permission import IsHospital, IsSuperuser
from apps.users.serializers import HospitalModelSerializer, HospitalUpdateDeleteModelSerializer


@extend_schema(tags=["Hospitals List"])
class HospitalListCreateView(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer
    permission_classes = [IsSuperuser]


@extend_schema(tags=["Hospital Detail"])
class HospitalRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalUpdateDeleteModelSerializer
    permission_classes = [IsHospital | IsSuperuser]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
