from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from apps.users.models import Product, CartItem, Order, OrderItem, Wallet
from apps.users.serializers.pharmacy import ProductSerializer, CartItemSerializer, OrderSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        if product.stock < int(quantity):
            return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        client = request.data.get('client')
        cart_items = CartItem.objects.filter(client_id=client)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.total_price for item in cart_items)

        client_wallet = Wallet.objects.get(user=cart_items.first().client.user.user)
        if client_wallet.balance < total_amount:
            return Response({'error': 'Insufficient balance in wallet'}, status=status.HTTP_400_BAD_REQUEST)

        client_wallet.balance -= total_amount
        client_wallet.save()

        order = Order.objects.create(client_id=client, total_amount=total_amount, payment_status=True)

        pharmacy_wallets = {}
        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise ValueError(f"Not enough stock for {product.name}")

            product.stock -= cart_item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price
            )

            pharmacy = product.pharmacy
            if pharmacy not in pharmacy_wallets:
                pharmacy_wallets[pharmacy] = Wallet.objects.get(user=pharmacy.user.user)

            pharmacy_wallets[pharmacy].balance += cart_item.total_price

        for wallet in pharmacy_wallets.values():
            wallet.save()

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
