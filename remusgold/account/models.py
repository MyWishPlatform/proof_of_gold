from bip32utils import BIP32Key
from eth_keys import keys

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from django.template.loader import render_to_string
from django.core.signing import Signer
from rest_framework.authtoken.models import Token
from django.core.signing import Signer
from django.core.mail import send_mail
from django.core.mail import get_connection

from remusgold.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD
from remusgold.settings import ALLOWED_HOSTS
from remusgold.account.api import get_root_key
from remusgold.templates.email.activation_letter_body2 import activation_body


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address',
    max_length=255, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    billing_address = models.OneToOneField('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.OneToOneField('ShippingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    btc_address = models.CharField(max_length=50, null=True, default=None)
    eth_address = models.CharField(max_length=50, null=True, default=None)
    agent = models.CharField(max_length=150, null=True, default=None)
    geolocation = models.CharField(max_length=150, null=True, default=None)
    code = models.CharField(max_length=6, null=True, default=None)

    def generate_keys(self):
        eth_btc_root_pub_key = get_root_key()
        eth_btc_root_key = BIP32Key.fromExtendedKey(eth_btc_root_pub_key, public=True)
        eth_btc_child_key = eth_btc_root_key.ChildKey(self.id)
        btc_address = eth_btc_child_key.Address()
        eth_address = keys.PublicKey(eth_btc_child_key.K.to_string()).to_checksum_address().lower()
        self.btc_address = btc_address
        self.eth_address = eth_address
        self.save()


def user_registrated_dispatcher(sender, instance, created, **kwargs):
    print('got here')
    if created:
        send_activation_notification(instance)


post_save.connect(user_registrated_dispatcher, sender=AdvUser)


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=80, null=True, blank=True)
    full_address = models.CharField(max_length=60, null=True, blank=True)
    town = models.CharField(max_length=15, null=True, blank=True)
    county = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=80, null=True, blank=True)
    full_address = models.CharField(max_length=60, null=True, blank=True)
    town = models.CharField(max_length=15, null=True, blank=True)
    county = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def get_mail_connection():
    return get_connection(
        host=EMAIL_HOST,
        port=EMAIL_PORT,
        username=EMAIL_HOST_USER,
        password=EMAIL_HOST_PASSWORD,
        use_tls=EMAIL_USE_TLS,
    )

def send_activation_notification(user):
    #user = AdvUser.objects.get(id=id)
    signer = Signer()
    token=signer.sign(user.username)
    connection = get_mail_connection()
    html_body = activation_body.format(
        token=token,
    )
    send_mail(
        'Registration on Proof of Gold',
        '',
        EMAIL_HOST_USER,
        [user.email],
        connection=connection,
        html_message=html_body,
        )
