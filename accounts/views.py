import logging
import os

import stripe
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomerProfile, User
from .serializers import RegisterSerializer

stripe.api_key = os.environ.get("STRIPE_API_TEST_SK")

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class RetrieveProfileInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            # verify customer profile
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "email": request.user.email,
                    "success": True,
                },
            )

        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str(
                        "Unknown issue occured retrieving profile information."
                    ),
                    "success": False,
                },
            )


class DeleteProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            # verify customer profile
            customer_profile = CustomerProfile.objects.get(user=request.user)
            deleted_stripe_customer = stripe.Customer.delete(
                customer_profile.stripe_customer_id
            )
            customer_profile.delete()
            user = User.objects.get(email=request.user.email)
            user.is_active = False
            user.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "success": True,
                },
            )

        except Exception as e:
            logger.error("Unknown Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str(
                        "Unknown issue occured deleting customer information."
                    ),
                    "success": False,
                },
            )
