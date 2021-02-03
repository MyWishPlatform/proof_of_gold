from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from django.template.loader import render_to_string
from django.core.signing import Signer
from remusgold.settings import ALLOWED_HOSTS
from remusgold.templates.email import activation_letter_body
from rest_framework.authtoken.models import Token
from django.core.signing import Signer

# Create your models here.


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address',
    max_length=255, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    billing_address = models.OneToOneField('BillingAddress', on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.OneToOneField('ShippingAddress', on_delete=models.CASCADE, blank=True, null=True)


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    company_name = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=40, null=True)
    street = models.CharField(max_length=20, null=True)
    house = models.CharField(max_length=20, null=True)
    town = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    zip_code = models.IntegerField(null=True)


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    company_name = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=40, null=True)
    street = models.CharField(max_length=20, null=True)
    house = models.CharField(max_length=20, null=True)
    town = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    zip_code = models.IntegerField(null=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



user_registrated = Signal(providing_args=['instance'])

#MAIL TESTING
def send_mail(email):
    connection = get_mail_connection()
    html_body = activation_html_body.format(
        tokens_purchased=self.usd_amount,
    )
    send_mail(
        'Registration on Proof of Gold',
        '',
        EMAIL_HOST_USER,
        [email],
        connection=connection,
        html_message=html_body,
        )


def get_mail_connection():
    return get_connection(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=EMAIL_USE_TLS,
    )


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispatcher)

def send_activation_notification(id):
    user = AdvUser.objects.get(id=id)
    signer = Signer()
    if ALLOWED_HOSTS:
        host='http://'+ALLOWED_HOSTS[0]
    else:
        host='http://localhost:8000'
    full_link = host+'/api/v1/account/register/activate'+signer.sign(user.username)
    connection = get_mail_connection()
    html_body = activation_letter_body.format(
        link=full_link,
    )
    send_mail(
        'Registration on Proof of Gold',
        '',
        EMAIL_HOST_USER,
        [user.email],
        connection=connection,
        html_message=html_body,
        )