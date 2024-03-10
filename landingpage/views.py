import logging

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LandingPage, NewsletterSignup
from .serializers import LandingPageSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GetLandingPageData(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            landing_page = LandingPage.objects.all()[0]
            landing_page_serializer = LandingPageSerializer(landing_page, many=False)

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "landing_page": landing_page_serializer.data,
                    "success": True,
                },
            )
        except Exception as e:
            logger.error("Error. Message: {}.".format(str(e)))
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": str(
                        "Error occurred while retrieving landing page data."
                    ),
                    "success": False,
                },
            )


class CreateNewsletterSignup(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            data = request.data
            email = data["email"]
            validate_email(email)
            if NewsletterSignup.objects.filter(email=email).exists():
                raise ValidationError("Email already exists for newsletter!")
            created_newsletter_signup = NewsletterSignup(email=email)
            created_newsletter_signup.save()
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
                    "message": e.message,
                    "success": False,
                },
            )
