from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from apps.users.filters import TopDoctor
from apps.users.models import Doctor
from apps.users.permission import IsDoctor, IsSuperuser, IsClient
from apps.users.serializers import DoctorModelSerializer, DoctorUpdateDeleteModelSerializer


@extend_schema(tags=['Doctor list'])
class DoctorListCreateView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorModelSerializer
    permission_classes = [IsDoctor | IsSuperuser | IsClient]
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_class = TopDoctor
    search_fields = ['name', 'category__name']


@extend_schema(tags=['Doctor Detail'])
class DoctorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorUpdateDeleteModelSerializer
    permission_classes = [IsDoctor | IsSuperuser]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
