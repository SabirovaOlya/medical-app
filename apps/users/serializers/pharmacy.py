from rest_framework.serializers import ModelSerializer

from apps.users.models import Product, CartItem, Order, OrderItem


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'pharmacy']
        read_only_fields = ['id']


class CartItemSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'client', 'product', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']


class OrderItemSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']
        read_only_fields = ['id', 'total_price']


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'items', 'total_amount', 'payment_status', 'order_date']
        read_only_fields = ['id', 'total_amount', 'payment_status', 'order_date']
