from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from apps.users.models import Client
from apps.users.permission import IsClient, IsSuperuser
from apps.users.serializers import ClientModelSerializer, ClientUpdateDeleteModelSerializer


@extend_schema(tags=['Clients List'])
class ClientListCreateView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientModelSerializer
    permission_classes = [IsSuperuser]


@extend_schema(tags=['Client Detail'])
class ClientsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateDeleteModelSerializer
    permission_classes = [IsClient | IsSuperuser]

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
