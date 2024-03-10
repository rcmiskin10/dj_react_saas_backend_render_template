import datetime
import logging
import os

import stripe
from accounts.models import CustomerProfile
from payments.models import Product
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductPrice
from .serializers import ProductSerializer

stripe.api_key = os.environ.get("STRIPE_API_TEST_SK")

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Add payment method
class AddPaymentMethod(APIView):
    permission_classes = [IsAuthenticated]

    def post(post, request, format=None):
        data = request.data
        payment_method_id = data["payment_method_id"]

        try:
            customer_profile = CustomerProfile.objects.get(user=request.user)
            customers_current_stripe_payment_method_id = (
                customer_profile.stripe_payment_method_id
            )
            if customers_current_stripe_payment_method_id is None:
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer_profile.stripe_customer_id,
                )
            else:
                stripe.PaymentMethod.detach(customers_current_stripe_payment_method_id)
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer_profile.stripe_customer_id,
                )

            # update customer profile with new values.
            customer_profile.stripe_payment_method_id = payment_method_id
            customer_profile.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "data": {
                        "customer_id": customer_profile.stripe_customer_id,
                        "success": True,
                    }
                },
            )

        except stripe.error.StripeError as e:
            logger.error(
                "Error!\nStatus: {}.\nCode: {}.\nParam: {}.\nMessage: {}.\n".format(
                    e.http_status, e.code, e.param, e.user_message
                )
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "There was an issue adding a payment method.",
                    "success": False,
                },
            )
        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str("Unknown issue occured adding a payment method."),
                    "success": False,
                },
            )


# Update subscription plan
class UpdateSubscription(APIView):
    permission_classes = [IsAuthenticated]

    def post(post, request, format=None):
        data = request.data
        selected_product_id = data["selected_product_id"]
        selected_product = ProductPrice.objects.get(product_id=selected_product_id)
        new_price_id = selected_product.stripe_price_id

        customer_profile = CustomerProfile.objects.get(user=request.user)

        try:
            customers_current_subscription_id = customer_profile.stripe_subscription_id
            new_subscription = None
            if customers_current_subscription_id is not None:
                subscription = stripe.Subscription.retrieve(
                    customers_current_subscription_id
                )
                stripe.Subscription.modify(
                    customers_current_subscription_id,
                    cancel_at_period_end=False,
                    proration_behavior="none",
                    default_payment_method=customer_profile.stripe_payment_method_id,
                    items=[
                        {
                            "id": subscription["items"]["data"][0].id,
                            "price": new_price_id,
                        }
                    ],
                )
            else:
                new_subscription = stripe.Subscription.create(
                    customer=customer_profile.stripe_customer_id,
                    default_payment_method=customer_profile.stripe_payment_method_id,
                    items=[{"price": new_price_id}],
                )
            # update customer profile with new values.
            product_price = ProductPrice.objects.get(stripe_price_id=new_price_id)
            customer_profile.product = product_price.product
            if new_subscription is not None:
                customer_profile.stripe_subscription_id = new_subscription.id
            customer_profile.save()

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "data": {
                        "customer_id": customer_profile.stripe_customer_id,
                        "success": True,
                    }
                },
            )
        except stripe.error.StripeError as e:
            logger.error(
                "Error!\nStatus: {}.\nCode: {}.\nParam: {}.\nMessage: {}.\n".format(
                    e.http_status, e.code, e.param, e.user_message
                )
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "There was an issue updating subscription plan.",
                    "success": False,
                },
            )
        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str("Unknown issue occured updating subscription plan."),
                    "success": False,
                },
            )


class RetrieveBillingInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get_current_payment_method_details(self, customer_payment_method):
        if customer_payment_method != None:
            return {
                "type": customer_payment_method.type,
                "brand": customer_payment_method.card.brand,
                "last4": customer_payment_method.card.last4,
                "exp_month": customer_payment_method.card.exp_month,
                "exp_year": customer_payment_method.card.exp_year,
            }
        else:
            return None

    def get(self, request, format=None):
        try:
            # verify customer profile
            customer_profile = CustomerProfile.objects.get(user=request.user)
            customers_current_product = customer_profile.product
            customers_current_product_serializer = ProductSerializer(
                customers_current_product, many=False
            )
            products = Product.objects.all()
            products_serializer = ProductSerializer(products, many=True)
            customer_subscription = None
            customer_payment_method = None
            if customer_profile.stripe_subscription_id is not None:
                customer_subscription = stripe.Subscription.retrieve(
                    customer_profile.stripe_subscription_id
                )
                customer_payment_method = stripe.PaymentMethod.retrieve(
                    customer_profile.stripe_payment_method_id
                )

            if customer_profile.stripe_payment_method_id is not None:
                customer_payment_method = stripe.PaymentMethod.retrieve(
                    customer_profile.stripe_payment_method_id
                )

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "subscription_start": (
                        datetime.datetime.fromtimestamp(
                            customer_subscription.current_period_start
                        ).strftime("%Y-%m-%d")
                        if customer_subscription is not None
                        else None
                    ),
                    "subscription_end": (
                        datetime.datetime.fromtimestamp(
                            customer_subscription.current_period_end
                        ).strftime("%Y-%m-%d")
                        if customer_subscription is not None
                        else None
                    ),
                    "customers_current_payment_method_details": self.get_current_payment_method_details(
                        customer_payment_method
                    ),
                    "customers_current_product": (
                        customers_current_product_serializer.data
                        if customers_current_product is not None
                        else None
                    ),
                    "all_product_choices": products_serializer.data,
                    "success": True,
                },
            )
        except stripe.error.StripeError as e:
            logger.error(
                "Error!\nStatus: {}.\nCode: {}.\nParam: {}.\nMessage: {}.\n".format(
                    e.http_status, e.code, e.param, e.user_message
                )
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "There was an issue retrieving billing information.",
                    "success": False,
                },
            )
        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str(
                        "Unknown issue occured retrieving billing information."
                    ),
                    "success": False,
                },
            )


class RetrieveAllProducts(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            products = Product.objects.all()
            products_serializer = ProductSerializer(products, many=True)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "all_product_choices": products_serializer.data,
                    "success": True,
                },
            )
        except stripe.error.StripeError as e:
            logger.error(
                "Error!\nStatus: {}.\nCode: {}.\nParam: {}.\nMessage: {}.\n".format(
                    e.http_status, e.code, e.param, e.user_message
                )
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "There was an issue retrieving billing information.",
                    "success": False,
                },
            )
        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str("Unknown issue occured retrieving products."),
                    "success": False,
                },
            )


class RetrieveProductInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            data = request.query_params

            product_id = data["product_id"]

            product = Product.objects.get(id=product_id)
            product_serializer = ProductSerializer(product, many=False)
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "product": product_serializer.data,
                    "success": True,
                },
            )
        except stripe.error.StripeError as e:
            logger.error(
                "Error!\nStatus: {}.\nCode: {}.\nParam: {}.\nMessage: {}.\n".format(
                    e.http_status, e.code, e.param, e.user_message
                )
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": "There was an issue retrieving billing information.",
                    "success": False,
                },
            )
        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str(
                        "Unknown issue occured retrieving product information."
                    ),
                    "success": False,
                },
            )
