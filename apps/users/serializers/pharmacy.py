from rest_framework import serializers

from apps.users.models import Product, CartItem, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'pharmacy']


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'cart_item_ids', 'total_amount', 'payment_status', 'order_date', 'items']
        read_only_fields = ['total_amount', 'payment_status', 'order_date']

    # def validate_cart_item_ids(self, value):
    #     client = self.context['request'].user.profile.client
    #     cart_items = CartItem.objects.filter(id__in=value, client=client)
    #
    #     # if len(cart_items) != len(value):
    #     #     raise serializers.ValidationError("Some cart items are invalid or do not belong to the user.")
    #
    #     return value
