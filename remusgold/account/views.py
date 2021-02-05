import json
from datetime import timedelta
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from django.shortcuts import render
from django.contrib.auth.password_validation import validate_password, ValidationError, MinimumLengthValidator, NumericPasswordValidator
from django.contrib.auth import authenticate
from django.core.signing import Signer
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404
from django_rest_resetpassword.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import get_connection
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings

from remusgold.account.models import AdvUser, ShippingAddress, BillingAddress
from remusgold.account.serializers import PatchSerializer, PatchShippingAddressSerializer, PatchBillingAddressSerializer
from remusgold.account.models import get_mail_connection
from remusgold.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_PASSWORD


from django_rest_resetpassword.serializers import EmailSerializer, PasswordTokenSerializer, TokenSerializer
from django_rest_resetpassword.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field
from django_rest_resetpassword.signals import reset_password_token_created, pre_password_reset, post_password_reset


signer = Signer()

register_response = openapi.Response(
    description="Response with registered user",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
)

login_response = openapi.Response(
    description="Response with logged in user",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'token': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )
)

get_response = openapi.Response(

    description="Response with user info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'billing_address_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'shipping_address_id': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    )
)

address_response = openapi.Response(

    description="Response with user's address info",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'company_name': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            'country': openapi.Schema(type=openapi.TYPE_STRING),
            'street': openapi.Schema(type=openapi.TYPE_STRING),
            'house': openapi.Schema(type=openapi.TYPE_STRING),
            'town': openapi.Schema(type=openapi.TYPE_STRING),
            'state': openapi.Schema(type=openapi.TYPE_STRING),
            'zip-code': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    )
)

class GetView(APIView):
    #permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="get single user's info",
        responses={200: get_response},
    )
    def get(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        shipping_address_id, billing_address_id = get_addresses(user)
        response_data = {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name,
            'last_name': user.last_name, 'billing_address_id': billing_address_id, 'shipping_adress_id': shipping_address_id}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="update single user's info",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password':openapi.Schema(type=openapi.TYPE_STRING),
                'new_password':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: get_response},
    )
    def patch(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        shipping_address_id, billing_address_id = get_addresses(user)
        if request.data.get('new_password'):
            new_password = request.data.get('new_password')
            try:
                validate_password(new_password, new_password,
                                  password_validators=[MinimumLengthValidator(min_length=8), NumericPasswordValidator])
            except ValidationError:
                return Response('Password is not valid', status=status.HTTP_401_UNAUTHORIZED)
            if new_password.isalpha():
                return Response('Password is not valid', status=status.HTTP_401_UNAUTHORIZED)
        serializer = PatchSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user = AdvUser.objects.get(id=token.user_id)
        response_data = {'id': user.id, 'username': user.username, 'email': user.email, 'first_name': user.first_name,
            'last_name': user.last_name, 'billing_address_id': billing_address_id, 'shipping_adress_id': shipping_address_id}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class RegisterView(APIView):

    @swagger_auto_schema(
        operation_description="register user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'email'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: register_response},
    )
    def post(self, request):
        request_data_init = request.data
        try:
            username = request_data_init['username']
            email = request_data_init['email']
            password = request_data_init['password']
        except:
            request_data = request_data_init['_content']
            request_data = json.loads(request_data)
            print(f'request_data: {request_data}')
            username = request_data['username']
            email = request_data['email']
            password = request_data['password']
        try:
            validate_password(password, password, password_validators=[MinimumLengthValidator(min_length=8), NumericPasswordValidator])
        except ValidationError:
            return Response('Password is not valid', status=status.HTTP_401_UNAUTHORIZED)
        if password.isalpha():
            return Response('Password is not valid', status=status.HTTP_401_UNAUTHORIZED)
        user = AdvUser.objects.create_user(username, email, password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        response_data = {'status': 'OK'}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class ShippingView(APIView):
    #permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="get single user's address",
        responses={200: address_response},
    )
    def get(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        try:
            shipping_address = user.shipping_address
            response_data = {'first_name': shipping_address.first_name, 'last_name': shipping_address.last_name,
                'company_name': shipping_address.company_name, 'country': shipping_address.country, 'street': shipping_address.street,
                'house': shipping_address.house, 'town': shipping_address.town, 'state': shipping_address.state, 'zip_code': shipping_address.zip_code}
            print('res:', response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return None

    @swagger_auto_schema(
        operation_description="update single user's address",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'company_name': openapi.Schema(type=openapi.TYPE_STRING),
            'country': openapi.Schema(type=openapi.TYPE_STRING),
            'street': openapi.Schema(type=openapi.TYPE_STRING),
            'house': openapi.Schema(type=openapi.TYPE_STRING),
            'town': openapi.Schema(type=openapi.TYPE_STRING),
            'state': openapi.Schema(type=openapi.TYPE_STRING),
            'zip-code': openapi.Schema(type=openapi.TYPE_NUMBER),
        }),
        responses={200: address_response},
    )
    def patch(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        serializer = PatchShippingAddressSerializer(user.shipping_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user = AdvUser.objects.get(id=token.user_id)
        response_data = {'first_name': user.shipping_address.first_name, 'last_name': user.shipping_address.last_name,
            'company_name': user.shipping_address.company_name, 'country': user.shipping_address.country, 'street': user.shipping_address.street,
            'house': user.shipping_address.house, 'town': user.shipping_address.town, 'state': user.shipping_address.state, 'zip_code': user.shipping_address.zip_code}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="creat single user's address",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            }),
        responses={200: 'OK'},
    )
    def post(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        user.shipping_address = ShippingAddress()
        user.shipping_address.save()
        user.save()
        response_data = {'OK'}
        return Response(response_data, status=status.HTTP_200_OK)


class BillingView(APIView):
    #permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="get single user's address",
        responses={200: address_response},
    )
    def get(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        try:
            billing_address = user.billing_address
            response_data = {'first_name': billing_address.first_name, 'last_name': billing_address.last_name,
                'company_name': billing_address.company_name, 'country': billing_address.country, 'street': billing_address.street,
                'house': billing_address.house, 'town': billing_address.town, 'state': billing_address.state, 'zip_code': billing_address.zip_code}
            print('res:', response_data)
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            return None

    @swagger_auto_schema(
        operation_description="update single user's address",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            'company_name': openapi.Schema(type=openapi.TYPE_STRING),
            'country': openapi.Schema(type=openapi.TYPE_STRING),
            'street': openapi.Schema(type=openapi.TYPE_STRING),
            'house': openapi.Schema(type=openapi.TYPE_STRING),
            'town': openapi.Schema(type=openapi.TYPE_STRING),
            'state': openapi.Schema(type=openapi.TYPE_STRING),
            'zip-code': openapi.Schema(type=openapi.TYPE_NUMBER),
        }),
        responses={200: address_response},
    )
    def patch(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        serializer = PatchBillingAddressSerializer(user.billing_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user = AdvUser.objects.get(id=token.user_id)
        response_data = {'first_name': user.billing_address.first_name, 'last_name': user.billing_address.last_name,
            'company_name': user.billing_address.company_name, 'country': user.billing_address.country, 'street': user.billing_address.street,
            'house': user.billing_address.house, 'town': user.billing_address.town, 'state': user.billing_address.state, 'zip_code': user.billing_address.zip_code}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="creat single user's address",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
            }),
        responses={200: 'OK'},
    )
    def post(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        user.billing_address = BillingAddress()
        user.billing_address.save()
        user.save()
        response_data = {'OK'}
        return Response(response_data, status=status.HTTP_200_OK)

def get_addresses(user):
    try:
        shipping_address_id = user.shipping_address_id
    except:
        shipping_address_id = None
    try:
        billing_address_id = user.billing_address_id
    except:
        billing_address_id = None
    return shipping_address_id, billing_address_id


class ObtainAuthTokenWithId(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print('WTF??')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_id = user.id
        username = user.username
        shipping_address_id, billing_address_id = get_addresses(user)
        token, created = Token.objects.get_or_create(user=user)
        if user.is_activated():
            return Response({'token': token.key, 'username': username, 'id':user.id, 'email': user.email,
                         'first_name': user.first_name, 'last_name': user.last_name,
                         'billing_address_id': billing_address_id, 'shipping_adress_id': shipping_address_id})
        else:
            return Response({'status': 'User is not activated'})


@api_view(http_method_names=['GET'])
def register_activate(request, sign):
    try:
        username=signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user=get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        return Response('already activated', status=status.HTTP_401_UNAUTHORIZED)
    else:
        user.is_activated=True
        user.save()
        token = Token.objects.get(user_id=user.id)
        return Response({'token': token.key, 'username': username, 'id': user.id, 'email': user.email,
                     'first_name': user.first_name, 'last_name': user.last_name,
                     'billing_address_id': billing_address_id, 'shipping_adress_id': shipping_address_id})




from remusgold.templates.email.user_reset_password import reset_body

# FROM NOW, I DON'T HAVE ANY FUCKING IDEA WHAT IS HAPPENING HERE, PROCEED ON YOUR OWN RISK

HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')

class HttpRes(object):
    def __init__(self, user=None, **args):
        self.response = {
            "status": args.get('status', True),
            "error": args.get('error', []),
            "data": args.get('data', []),
            "message": args.get('message', 'Operation was Successful')
        }


class ResetPasswordRequestToken(GenericAPIView):
    """
    An Api View which provides a method to request a password reset token based on an e-mail address

    Sends a signal reset_password_token_created when a reset token was created
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # before we continue, delete all existing expired tokens
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now(
        ) - timedelta(hours=password_reset_token_validation_time)

        # delete all tokens where created_at < now - 24 hours
        clear_expired(now_minus_expiry_time)

        # find a user by email address (case insensitive search)
        users = AdvUser.objects.filter(
            **{'{}__iexact'.format(get_password_reset_lookup_field()): email})

        active_user_found = False

        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.eligible_for_reset():
                active_user_found = True

        # No active user found, raise a validation error
        # but not if DJANGO_REST_RESETPASSWORD_NO_INFORMATION_LEAKAGE == True
        if not active_user_found and not getattr(settings, 'DJANGO_REST_RESETPASSWORD_NO_INFORMATION_LEAKAGE', False):
            raise exceptions.ValidationError({
                'email': [_(
                    "There is no active user associated with this e-mail address or the password can not be changed")],
            })

        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.eligible_for_reset():
                # define the token as none for now
                token = None

                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent=request.META.get(
                            HTTP_USER_AGENT_HEADER, ''),
                        ip_address=request.META.get(
                            HTTP_IP_ADDRESS_HEADER, ''),
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                reset_password_token_created.send(
                    sender=self.__class__, instance=self, reset_password_token=token)
        # done
        response_format = HttpRes().response
        response_format['message'] = "A password reset token has been sent to the provided email address"
        response_format['status'] = True
        response_format['error'] = []
        return Response(response_format)

reset_password_request_token = ResetPasswordRequestToken.as_view()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-validate'), reset_password_token.key)
    }
    email_plaintext_message = context['reset_password_url']

    connection = get_mail_connection()

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Proof of Gold"),
        # message:
        email_plaintext_message,
        # from:
        EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
        # connection
        connection=connection,
    )
    #msg.attach_alternative(email_html_message, "text/html")
    msg.send()


class ResetPasswordValidateToken(GenericAPIView):
    """
    An Api View which provides a method to verify that a token is valid
    """
    throttle_classes = ()
    permission_classes = ()
    serializer_class = TokenSerializer

    def get(self, request, token):
        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(
            key=token).first()

        if reset_password_token is None:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + \
            timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': 'OK'})

reset_password_validate_token = ResetPasswordValidateToken.as_view()

