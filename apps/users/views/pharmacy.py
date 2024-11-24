from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, serializers
from rest_framework.filters import SearchFilter

from apps.users.models import Product, CartItem, Order, OrderItem, Wallet
from apps.users.permission import IsClient, IsSuperuser, IsPharmacy
from apps.users.serializers.pharmacy import ProductSerializer, CartItemSerializer, OrderSerializer


@extend_schema(tags=['Product list'])
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsClient | IsSuperuser | IsPharmacy]
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ['name', 'description']


@extend_schema(tags=['Product Create'])
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsPharmacy | IsSuperuser]


@extend_schema(tags=['Product Detail'])
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsClient | IsSuperuser | IsPharmacy]


class CartItemListView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsClient | IsSuperuser]

    def get_queryset(self):
        return CartItem.objects.filter(client=self.request.user.profile.client)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.profile.client)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsClient | IsSuperuser]

    def get_queryset(self):
        return CartItem.objects.filter(client=self.request.user.profile.client)


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsClient | IsSuperuser]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user.profile.client)

    @transaction.atomic
    def perform_create(self, serializer):
        client = self.request.user.profile.client
        cart_item_ids = serializer.validated_data.pop('cart_item_ids')
        cart_items = CartItem.objects.filter(id__in=cart_item_ids, client=client)

        if not cart_items.exists():
            raise serializers.ValidationError("Selected cart items are empty.")

        total_amount = sum(item.total_price for item in cart_items)

        wallet = Wallet.objects.get(user=client.user.user)
        if wallet.balance < total_amount:
            raise serializers.ValidationError("Insufficient wallet balance.")

        wallet.balance -= total_amount
        wallet.save()

        order = serializer.save(client=client, total_amount=total_amount, payment_status=True)

        for cart_item in cart_items:
            product = cart_item.product
            if product.stock < cart_item.quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}.")
            product.stock -= cart_item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price,
            )

        cart_items.delete()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsClient | IsSuperuser]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user.profile.client)
