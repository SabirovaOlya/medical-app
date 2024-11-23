from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.users.models import Pharmacy
from apps.users.permission import IsPharmacy, IsSuperuser, IsClient
from apps.users.serializers import PharmacyModelSerializer, PharmacyUpdateDeleteModelSerializer


@extend_schema(tags=['Pharmacies List'])
class PharmacyListCreateView(ListAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyModelSerializer
    permission_classes = [IsPharmacy | IsSuperuser | IsClient]
    filter_backends = (SearchFilter,)
    search_fields = ['name']


@extend_schema(tags=['Pharmacy Detail'])
class PharmaciesRetrieveView(RetrieveAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyUpdateDeleteModelSerializer
    permission_classes = [IsPharmacy | IsSuperuser]
