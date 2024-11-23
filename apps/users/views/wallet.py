from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.users.models import Wallet
from apps.users.permission import IsSuperuser
from apps.users.serializers import WalletModelSerializer


@extend_schema(tags=['Wallets List'])
class WalletListView(ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletModelSerializer
    permission_classes = [IsSuperuser]


@extend_schema(tags=['Wallet Create'])
class WalletCreateView(CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletModelSerializer
