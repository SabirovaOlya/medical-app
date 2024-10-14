from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User, Hospital, Pharmacy, Doctor, Client, Profile


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
class PharmacyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Hospital)
class HospitalModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Pharmacy)
class PharmacyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Doctor)
class PharmacyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class PharmacyModelAdmin(admin.ModelAdmin):
    pass
