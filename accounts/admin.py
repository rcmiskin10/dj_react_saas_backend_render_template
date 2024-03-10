from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomerProfile, User


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "email",
        "date_joined",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_superuser",
                    "is_staff",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


class CustomerProfileAdmin(admin.ModelAdmin):
    model = CustomerProfile
    list_display = (
        "user",
        "stripe_customer_id",
        "stripe_subscription_id",
        "stripe_payment_method_id",
        "product",
    )


admin.site.register(CustomerProfile, CustomerProfileAdmin)
