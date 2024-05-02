from celery import shared_task
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


@shared_task
def send_activation_email(user_id, domain):
    from .models import CustomUser
    user = CustomUser.objects.get(pk=user_id)
    subject = 'Activate your account'
    context = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    }
    message = render_to_string('registration/account_activation_email.html', context)
    email = EmailMessage(
        subject,
        message,
        to=[user.email]
    )
    email.content_subtype = 'html'
    email.send()

    return message


@shared_task
def addition(a, b):
    print(a, b)
    return a + b
