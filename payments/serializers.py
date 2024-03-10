from rest_framework import serializers

from .models import Product, ProductDescriptionItem, ProductPrice


class ProductDescriptionItem(serializers.ModelSerializer):
    class Meta:
        model = ProductDescriptionItem
        fields = ["description"]


class ProductPrice(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ["price", "interval", "type"]


class ProductSerializer(serializers.ModelSerializer):
    descriptions = ProductDescriptionItem(many=True)
    prices = ProductPrice(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "tier", "descriptions", "prices"]
