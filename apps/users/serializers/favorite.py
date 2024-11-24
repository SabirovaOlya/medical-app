from rest_framework import serializers

from apps.users.models import FavoriteProduct


class FavoriteProductSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.user.user.username')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = FavoriteProduct
        fields = ['id', 'client', 'product', 'product_name', 'product_price', 'added_on']
