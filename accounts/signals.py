# accounts/signals.py

import logging
import smtplib

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    try:
        # send an e-mail to the user
        context = {
            "current_user": reset_password_token.user,
            "email": reset_password_token.user.email,
            "token": reset_password_token.key,
            "password_reset_url": "{}/{}/?token={}".format(
                settings.FRONTEND_URL,
                "reset-password",
                reset_password_token.key,
            ),
        }

        # render email text
        email_html_message = render_to_string(
            "email/password_reset_email.html", context
        )
        email_plaintext_message = render_to_string(
            "email/password_reset_email.txt", context
        )

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {title}".format(title=settings.SITE_NAME),
            # message:
            email_plaintext_message,
            # from:
            settings.DEFAULT_FROM_EMAIL,
            # to:
            [reset_password_token.user.email],
        )

        msg.attach_alternative(email_html_message, "text/html")
        msg.send(fail_silently=False)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except smtplib.SMTPException as se:
        logger.error("Error. Message: {}.".format(str(se)))
        raise ValidationError(
            "There was an SMTP exception trying to send reset password email."
        )

    except Exception as e:
        logger.error("Error. Message: {}.".format(str(e)))
        raise ValidationError("There was an error trying to send reset password email.")
