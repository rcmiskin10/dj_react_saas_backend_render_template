from django.contrib import admin

from .models import Product, ProductDescriptionItem, ProductPrice


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("id", "tier", "name", "stripe_product_id")


admin.site.register(Product, ProductAdmin)


class ProductDescriptionItemAdmin(admin.ModelAdmin):
    model = ProductDescriptionItem
    list_display = ("id", "product", "description")


admin.site.register(ProductDescriptionItem, ProductDescriptionItemAdmin)


class ProductPriceAdmin(admin.ModelAdmin):
    model = ProductPrice
    list_display = (
        "id",
        "get_product_name",
        "price",
        "interval",
        "type",
        "stripe_price_id",
    )

    def get_product_name(self, obj):
        return obj.product.name


admin.site.register(ProductPrice, ProductPriceAdmin)
