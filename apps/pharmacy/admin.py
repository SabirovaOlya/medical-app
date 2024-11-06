from django.contrib import admin

from apps.pharmacy.models import Product, Cart, CartItem


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    pass
