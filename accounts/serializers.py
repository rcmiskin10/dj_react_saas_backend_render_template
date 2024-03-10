import os

import stripe
from django.contrib.auth.password_validation import validate_password
from payments.models import Product
from rest_framework import serializers

from .models import CustomerProfile, User

stripe.api_key = os.environ.get("STRIPE_API_TEST_SK")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        # creating customer
        user = User.objects.create(
            email=validated_data["email"],
        )

        customer = stripe.Customer.create(
            email=validated_data["email"],
            metadata={
                "user_id": user.pk,
            },
            description="Created from ideaverify",
        )

        user.set_password(validated_data["password"])
        user.save()

        product = Product.objects.get(name="Free")

        # creating customer profile
        customer_profile = CustomerProfile(
            user=user, stripe_customer_id=customer.id, product=product
        )
        customer_profile.save()

        return user


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
