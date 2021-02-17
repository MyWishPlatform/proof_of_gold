from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.decorators import api_view

from remusgold.payments.models import Payment, Order
from remusgold.store.models import Item
from remusgold.account.models import AdvUser, Token
from remusgold.vouchers.models import Voucher
from remusgold.settings import ALLOWED_HOSTS
# Create your views here.


get_response = openapi.Response(
    description="Response with all user's payments",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Items(type=openapi.TYPE_OBJECT,
        properties={'payments': openapi.Schema(type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'user': openapi.Schema(type=openapi.TYPE_STRING),
            'item_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'item_name': openapi.Schema(type=openapi.TYPE_STRING),
            'item_images': openapi.Schema(type=openapi.TYPE_OBJECT),
            'quantity': openapi.Schema(type=openapi.TYPE_NUMBER),
            'created_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        }
    ), }
)
)
)

get_single_response = openapi.Response(
    description="Response with single user's payments",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'user': openapi.Schema(type=openapi.TYPE_STRING),
            'item_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            'item_name': openapi.Schema(type=openapi.TYPE_STRING),
            'item_images': openapi.Schema(type=openapi.TYPE_OBJECT),
            'quantity': openapi.Schema(type=openapi.TYPE_NUMBER),
            'created_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        }
    )
)

class GetPaymentsView(APIView):

    @swagger_auto_schema(
        operation_description="get all user's payments",
        responses={200: get_response},
    )
    def get(self, request, user_id):
        payment_list = []
        orders = Order.objects.filter(user_id=user_id).filter(status='PAID')
        for order in orders:
            payments = Payment.objects.filter(order=order)

            for payment in payments:
                item = payment.item
                payment_list.append({'item_id': item.id, 'item_name': item.name,
                'item_image': ALLOWED_HOSTS[0] + item.images.url, 'quantity': payment.quantity, 'created_date': payment.created_date.strftime("%m/%d/%Y, %H:%M:%S")})

        response_data = {'payments': payment_list,}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)

class GetSinglePaymentView(APIView):

    @swagger_auto_schema(
        operation_description="get single user's payment",
        responses={200: get_single_response},
    )
    def get(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        item = payment.item
        response_data = {'item_id': item.id, 'item_name': item.name, 'item_image': ALLOWED_HOSTS[0] + item.images.url,
                'quantity': payment.quantity, 'created_date': payment.created_date.strftime("%m/%d/%Y, %H:%M:%S")}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class CreatePaymentView(APIView):

    @swagger_auto_schema(
        operation_description="post user's payments",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'items': openapi.Schema(type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_OBJECT,
                    properties={
                       'item_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                       'quantity': openapi.Schema(type=openapi.TYPE_NUMBER),
                        },
                    ),),
                'currency': openapi.Schema(type = openapi.TYPE_STRING),
                'shipping_address': openapi.Schema(type=openapi.TYPE_OBJECT,
                    properties={
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'company_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'country': openapi.Schema(type=openapi.TYPE_STRING),
                        'full_address': openapi.Schema(type=openapi.TYPE_STRING),
                        'town': openapi.Schema(type=openapi.TYPE_STRING),
                        'county': openapi.Schema(type=openapi.TYPE_STRING),
                        'phone': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                    },)
                },
            ),
        responses={200: 'OK'},
    )
    def post(self, request, token):
        request_data = request.data
        print(request_data)
        usd_amount = 0
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        currency = request_data.get('currency')
        order = Order(user=user, currency = currency)
        order.save()
        for request in request_data.get('items'):
            item_id = request.get('item_id')
            quantity = request.get('quantity')
            payment = Payment(order=order, item_id=item_id, quantity=quantity)
            payment.save()

        order.get_required_amount()
        order.fix_rates()

        return Response('OK', status=status.HTTP_200_OK)