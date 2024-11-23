from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.users.models import Hospital
from apps.users.permission import IsHospital, IsSuperuser, IsClient
from apps.users.serializers import HospitalModelSerializer, HospitalUpdateDeleteModelSerializer


@extend_schema(tags=["Hospitals List"])
class HospitalListCreateView(ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalModelSerializer
    permission_classes = [IsHospital | IsSuperuser | IsClient]
    filter_backends = (SearchFilter,)
    search_fields = ['name']


@extend_schema(tags=["Hospital Detail"])
class HospitalRetrieveView(RetrieveAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalUpdateDeleteModelSerializer
    permission_classes = [IsHospital | IsSuperuser | IsClient]
