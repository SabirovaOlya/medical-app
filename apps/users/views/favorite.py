from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, DestroyAPIView

from apps.users.models import FavoriteProduct
from apps.users.serializers.favorite import FavoriteProductSerializer


@extend_schema(tags=['Favourite List'])
class FavoriteProductListCreateView(ListCreateAPIView):
    serializer_class = FavoriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(client__user=self.request.user.profile)

    def perform_create(self, serializer):
        client = self.request.user.profile.client
        product = serializer.validated_data.get('product')

        if FavoriteProduct.objects.filter(client=client, product=product).exists():
            raise ValidationError("This product is already in your favorites.")

        serializer.save(client=client)


@extend_schema(tags=['Favourite Delete'])
class FavoriteProductDeleteView(DestroyAPIView):
    serializer_class = FavoriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(client__user=self.request.user.profile)
