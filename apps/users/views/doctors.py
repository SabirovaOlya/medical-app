from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from apps.users.models import Doctor
from apps.users.serializers import DoctorModelSerializer, DoctorUpdateDeleteModelSerializer
from apps.users.views.permission import IsDoctor


@extend_schema(tags=['Doctor list'])
class DoctorListCreateView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorModelSerializer
    permission_classes = [IsDoctor]


@extend_schema(tags=['Doctor Detail'])
class DoctorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorUpdateDeleteModelSerializer
    permission_classes = [IsDoctor]
