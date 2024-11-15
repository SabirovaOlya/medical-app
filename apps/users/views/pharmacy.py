from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from apps.users.models import Product, CartItem, Order
from apps.users.serializers.pharmacy import ProductSerializer, CartItemSerializer, OrderSerializer


@extend_schema(tags=['Drugs List'])
class DrugListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(tags=['Drugs Detail'])
class DrugRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@extend_schema(tags=['Cart'])
class CartView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        # Filter to return only cart items for the current user’s cart
        client = self.request.user.profile.client
        return CartItem.objects.filter(cart__client=client)

    def update(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            raise ValidationError("Product ID is required.")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError("Product not found.")

        if product.stock < quantity:
            raise ValidationError("Insufficient stock for this product.")

        client = self.request.user.profile.client
        cart_item, created = CartItem.objects.get_or_create(cart=client.cart, product=product)

        with transaction.atomic():
            cart_item.quantity = quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        item_id = request.data.get("item_id")
        if not item_id:
            raise ValidationError("Item ID is required.")

        client = self.request.user.profile.client
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__client=client)
            cart_item.delete()
        except CartItem.DoesNotExist:
            raise ValidationError("Item not found in cart.")

        return Response({"detail": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Orders'])
class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        client = self.request.user.profile.client
        cart_items = CartItem.objects.filter(cart__client=client)

        if not cart_items.exists():
            raise ValidationError("No items in cart to create an order.")

        with transaction.atomic():
            # Check stock before creating an order
            for item in cart_items:
                if item.product.stock < item.quantity:
                    raise ValidationError(f"Insufficient stock for {item.product.name}.")

            # Create the order
            order = serializer.save(client=client)

            if not self.process_payment(order):
                raise ValidationError("Insufficient funds in wallet.")

            # Update stock levels and clear cart after successful payment
            for item in cart_items:
                item.product.stock -= item.quantity
                item.product.save()

            cart_items.delete()  # Clear cart after order is completed

    def process_payment(self, order):
        client_wallet = self.request.user.wallet
        total_cost = order.total_amount

        if client_wallet.balance >= total_cost:
            with transaction.atomic():
                client_wallet.balance -= total_cost
                client_wallet.save()

                # Assuming pharmacy has a wallet to credit
                pharmacy_wallet = order.items.first().product.pharmacy.user.wallet
                pharmacy_wallet.balance += total_cost
                pharmacy_wallet.save()

                order.payment_status = True
                order.save()
            return True
        return False


@extend_schema(tags=['Order Detail'])
class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user.profile.client)


@extend_schema(tags=['Payment'])
class PaymentCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        payment_method = request.data.get("payment_method", "Visa")

        try:
            order = Order.objects.get(id=order_id, client=self.request.user.profile.client)
        except Order.DoesNotExist:
            raise ValidationError("Order not found.")

        with transaction.atomic():
            if order.payment_status:
                raise ValidationError("Order is already paid.")

            if not self.process_payment(order):
                raise ValidationError("Insufficient balance in wallet.")

        return Response(
            {"message": "Payment successful", "order_id": order.id, "payment_method": payment_method},
            status=status.HTTP_200_OK
        )

    def process_payment(self, order):
        client_wallet = self.request.user.wallet
        pharmacy_wallet = order.items.first().product.pharmacy.user.wallet
        total_cost = order.total_amount

        if client_wallet.balance >= total_cost:
            with transaction.atomic():
                client_wallet.balance -= total_cost
                client_wallet.save()
                pharmacy_wallet.balance += total_cost
                pharmacy_wallet.save()
                order.payment_status = True
                order.save()
            return True
        return False
