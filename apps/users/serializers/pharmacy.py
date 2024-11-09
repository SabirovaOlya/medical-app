from rest_framework.serializers import ModelSerializer

from apps.users.models import Product, CartItem, Cart, Order, OrderItem, Payment


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'pharmacy']
        read_only_fields = ['id']


class CartItemSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        read_only_fields = ['id', 'total_price']


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'client', 'items', 'total']
        read_only_fields = ['id', 'total']


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


class PaymentSerializer(ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'amount', 'success', 'payment_date']
        read_only_fields = ['id', 'payment_date']
