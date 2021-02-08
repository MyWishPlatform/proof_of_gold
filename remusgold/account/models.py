from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from django.template.loader import render_to_string
from django.core.signing import Signer
from remusgold.settings import ALLOWED_HOSTS
from remusgold.templates.email.activation_letter_body import voucher_html_body, html_style
from rest_framework.authtoken.models import Token
from django.core.signing import Signer
from django.core.mail import send_mail
from django.core.mail import get_connection
from remusgold.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD
from remusgold.account.api import get_root_key

from bip32utils import BIP32Key
from eth_keys import keys
# Create your models here.


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address',
    max_length=255, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    billing_address = models.OneToOneField('BillingAddress', on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.OneToOneField('ShippingAddress', on_delete=models.CASCADE, blank=True, null=True)
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


post_save.connect(user_registrated_dispatcher, sender= AdvUser)


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    company_name = models.CharField(max_length=120, null=True)
    country = models.CharField(max_length=80, null=True)
    full_address = models.CharField(max_length=60, null=True)
    town = models.CharField(max_length=15, null=True)
    county = models.CharField(max_length=15, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    company_name = models.CharField(max_length=120, null=True)
    country = models.CharField(max_length=80, null=True)
    full_address = models.CharField(max_length=60, null=True)
    town = models.CharField(max_length=15, null=True)
    county = models.CharField(max_length=15, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#MAIL TESTING
def send_email(email):
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


def send_activation_notification(user):
    #user = AdvUser.objects.get(id=id)
    signer = Signer()
    if ALLOWED_HOSTS:
        host='http://'+ALLOWED_HOSTS[0]
    else:
        host='http://localhost:8000'
    full_link = host+'/api/v1/account/register/activate/'+signer.sign(user.username)
    connection = get_mail_connection()
    html_body = voucher_html_body.format(
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
