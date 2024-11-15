from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User, Hospital, Pharmacy, Doctor, Client, Profile, Booking, Wallet, Product, Order, \
    OrderItem, CartItem


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "phone_number", "password1", "password2", "email"),
            },
        ),
    )


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Hospital)
class HospitalModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Pharmacy)
class PharmacyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Doctor)
class DoctorModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Wallet)
class WalletModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    pass
