from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import viewsets
from rest_framework import status
from remusgold.account.models import AdvUser, ShippingAddress, BillingAddress
from rest_framework.authtoken.models import Token
from remusgold.account.serializers import PatchSerializer, PatchShippingAddressSerializer, PatchBillingAddressSerializer
from rest_framework.permissions import IsAuthenticated

register_response = openapi.Response(
    description="Response with registered user",
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
    def get(self, request, id):
        user = AdvUser.objects.get(id=id)
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
    def patch(self, request, id):
        user = AdvUser.objects.get(id=id)
        shipping_address_id, billing_address_id = get_addresses(user)
        serializer = PatchSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
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
        request_data = request.data
        username = request_data.get('username')
        email = request_data.get('email')
        password = request_data.get('password')
        user = AdvUser.objects.create_user(username, email, password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        response_data = {'id': user.id, 'username': user.username, 'email': user.email, 'token': token.key}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class ShippingView(APIView):
    #permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="get single user's address",
        responses={200: address_response},
    )
    def get(self, request, id):
        user = AdvUser.objects.get(id=id)
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
    def patch(self, request, id):
        user = AdvUser.objects.get(id=id)
        serializer = PatchShippingAddressSerializer(user.shipping_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user = AdvUser.objects.get(id=id)
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
    def post(self, request, id):
        user = AdvUser.objects.get(id=id)
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
    def get(self, request, id):
        user = AdvUser.objects.get(id=id)
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
    def patch(self, request, id):
        user = AdvUser.objects.get(id=id)
        serializer = PatchBillingAddressSerializer(user.billing_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user = AdvUser.objects.get(id=id)
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
    def post(self, request, id):
        user = AdvUser.objects.get(id=id)
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