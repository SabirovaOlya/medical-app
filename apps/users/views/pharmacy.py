from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import Product, Cart, CartItem, OrderItem, Order, Payment
from apps.users.serializers.pharmacy import ProductSerializer, CartSerializer, OrderSerializer, PaymentSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.profile.pharmacy)


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


# Cart Views
class CartRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.get(client=request.user.profile.client)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(client=request.user.profile.client)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            cart = Cart.objects.get(client=request.user.profile.client)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(client=request.user.profile.client)

        product = Product.objects.get(id=product_id)
        quantity = request.data.get('quantity', 1)

        # Update or create cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__client=request.user.profile.client)
            cart_item.delete()
        except CartItem.DoesNotExist:
            raise ValidationError("Item not found in cart.")

        cart = Cart.objects.get(client=request.user.profile.client)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Order Views
class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user.profile.client)

    def perform_create(self, serializer):
        cart = Cart.objects.get(client=self.request.user.profile.client)
        if not cart.items.exists():
            raise ValidationError("Cannot create an order with an empty cart.")

        order = serializer.save(client=self.request.user.profile.client, total_amount=cart.total)

        # Transfer cart items to order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        # Clear the cart
        cart.items.all().delete()
        return order


class OrderRetrieveView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user.profile.client)


# Payment Views
class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, client=request.user.profile.client)
        if order.payment_status:
            raise ValidationError("Order is already paid.")

        client_wallet = request.user.wallet
        if client_wallet.balance < order.total_amount:
            raise ValidationError("Insufficient balance.")

        # Deduct from client wallet and mark order as paid
        client_wallet.balance -= order.total_amount
        client_wallet.save()

        order.payment_status = True
        order.save()

        # Record payment
        payment = Payment.objects.create(
            order=order,
            payment_method=request.data.get('payment_method', 'Visa'),
            amount=order.total_amount,
            success=True,
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
