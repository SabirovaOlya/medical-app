from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from apps.users.models import Hospital
from apps.users.serializers import HospitalModelSerializer, HospitalUpdateDeleteModelSerializer
from apps.users.views.permission import IsHospital


@extend_schema(tags=["Hospitals List"])
class HospitalListCreateView(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer
    permission_classes = [IsHospital]


@extend_schema(tags=["Hospital Detail"])
class HospitalRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalUpdateDeleteModelSerializer
    permission_classes = [IsHospital]
