from rest_framework.serializers import ModelSerializer

from apps.users.models import Wallet


class WalletModelSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'card_number', 'expiry_date', 'cvc']
        read_only_fields = ['id']
