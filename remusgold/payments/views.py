from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.decorators import api_view

from remusgold.payments.models import Payment, Order
from remusgold.store.models import Item
from remusgold.account.models import AdvUser, Token, ShippingAddress
from remusgold.account.serializers import PatchShippingAddressSerializer
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
    def get(self, request, token):
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        orders = Order.objects.filter(user_id=user.id).filter(status='PAID')
        response_data = []
        for order in orders:
            if order.currency == 'eth':
                paid_by = 'ETH'
            elif order.currency == 'btc':
                paid_by = 'BTC'
            elif order.currency == 'usdc':
                paid_by = 'USDC'
            else:
                paid_by = 'Credit Card'
            current_order = {"id": order.id, "cost": order.required_usd_amount, 'date': order.created_date,
                'payment': paid_by, 'products': []}
            payments = Payment.objects.filter(order=order)

            for payment in payments:
                item = payment.item
                current_order['products'].append({'id': item.id, 'name': item.name,
                'img': ALLOWED_HOSTS[0] + item.images.url, 'count': payment.quantity, 'cost': item.price})
            response_data.append(current_order)
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
        previous = Order.objects.filter(user=user).filter(status="WAITING_FOR_PAYMENT")
        for prev in previous:
            if prev:
                prev.status="CANCELLED"
                prev.save()


        order = Order(user=user, currency = currency)
        order.save()
        shipping_address = request.data.get('shipping_address')
        if shipping_address:
            address = ShippingAddress()
            address.save()
            order.shipping_address = address
            order.save()
            serializer = PatchShippingAddressSerializer(address, data=request.data.get('shipping_address'), partial=True)
            if serializer.is_valid():
                serializer.save()
        for request in request_data.get('items'):
            item_id = request.get('item_id')
            quantity = request.get('quantity')
            payment = Payment(order=order, item_id=item_id, quantity=quantity)
            payment.save()

        order.get_required_amount()
        order.fix_rates()

        response_data = {"id": order.id}

        return Response(response_data, status=status.HTTP_200_OK)


class CheckActive(APIView):

    @swagger_auto_schema(
        operation_description="check user's payments status",
        responses={200: 'OK'},
    )
    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
            if order.status in ("PAID", "OVERPAYMENT"):
                return Response('PAID', status=status.HTTP_200_OK)
            elif order.status in ("UNDERPAYMENT", "CANCELLED"):
                return Response('CANCELLED', status=status.HTTP_200_OK)
            elif order.status in ("EXPIRED",):
                return Response('EXPIRED', status=status.HTTP_200_OK)
            else:
                return Response('WAITING_FOR_PAYMENT', status=status.HTTP_200_OK)
        except:
            return Response('NO_ORDER', status=status.HTTP_200_OK)
