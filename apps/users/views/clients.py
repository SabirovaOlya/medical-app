from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.users.models import Client
from apps.users.serializers import ClientModelSerializer, ClientUpdateDeleteModelSerializer


@extend_schema(tags=['Clients List'])
class ClientListCreateView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer


@extend_schema(tags=['Client Detail'])
class ClientsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateDeleteModelSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
