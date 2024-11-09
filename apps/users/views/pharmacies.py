from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from apps.users.models import Pharmacy
from apps.users.serializers import PharmacyModelSerializer, PharmacyUpdateDeleteModelSerializer


@extend_schema(tags=['Pharmacies List'])
class PharmacyListCreateView(ListAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyModelSerializer


@extend_schema(tags=['Pharmacy Detail'])
class PharmaciesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyUpdateDeleteModelSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
