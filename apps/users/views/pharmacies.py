from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from apps.users.models import Pharmacy
from apps.users.serializers import PharmacyModelSerializer, PharmacyUpdateDeleteModelSerializer
from apps.users.views.permission import IsPharmacy


@extend_schema(tags=['Pharmacies List'])
class PharmacyListCreateView(ListAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyModelSerializer
    permission_classes = [IsPharmacy]


@extend_schema(tags=['Pharmacy Detail'])
class PharmaciesRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyUpdateDeleteModelSerializer
    permission_classes = [IsPharmacy]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
