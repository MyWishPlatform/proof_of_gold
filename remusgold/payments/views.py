import datetime
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from remusgold.payments.models import Payment, Order
from remusgold.payments.paypal import GetOrder
from remusgold.store.models import Item
from remusgold.account.models import AdvUser, Token, ShippingAddress
from remusgold.account.serializers import PatchShippingAddressSerializer
from remusgold.vouchers.models import Voucher
from remusgold.settings import ALLOWED_HOSTS
from remusgold.payments.api import process_correct_payment
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
        orders = Order.objects.filter(user_id=user.id).filter(status__in=('PAID', 'OVERPAYMENT')).order_by('-id')
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
    '''
    deprecated view for getting single payment (frontend doesn't use it due to GetPaymentsView() is enough).
    #TODO: delete it if frontend will not use it for sure or update with changes similar to GetPaymentsView()
    '''
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

@method_decorator(csrf_exempt, name='dispatch')
class CreatePaymentView(APIView):
    '''
    Creating order, cancelling previous order if found.
    '''
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
                'currency': openapi.Schema(type=openapi.TYPE_STRING),
                'paypal_id': openapi.Schema(type=openapi.TYPE_STRING),
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
        token = Token.objects.get(key=token)
        user = AdvUser.objects.get(id=token.user_id)
        currency = request_data.get('currency')
        paypal_id = request.data.get('paypal_id')

        #cancelling previous order if found (only 1 order can be active for paying in crypto)
        previous = Order.objects.filter(user=user).filter(status="WAITING_FOR_PAYMENT")
        for prev in previous:
            if prev:
                prev.status="CANCELLED"
                prev.save()
                prev_payments = Payment.objects.filter(order=prev)
                for payment in prev_payments:
                    item = Item.objects.get(id=payment.item_id)
                    item.supply += payment.quantity
                    item.reserved -= payment.quantity
                    item.save()
        order = Order(user=user, currency=currency)
        order.save()

        #check paypal currency
        if currency == 'paypal':
            res = check_paypal(paypal_id)
            if res != True:
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        #saving payment unique ShippingAddress if it is not saved in user info
        shipping_address = request.data.get('shipping_address')
        if shipping_address:
            address = ShippingAddress()
            address.save()
            order.shipping_address = address
            order.save()
            serializer = PatchShippingAddressSerializer(address, data=request.data.get('shipping_address'), partial=True)
            if serializer.is_valid():
                serializer.save()

        #save items in order, calculate total amount and fix current rates
        for request in request_data.get('items'):
            item_id = request.get('item_id')
            quantity = request.get('quantity')
            payment = Payment(order=order, item_id=item_id, quantity=quantity)
            payment.save()
            item = Item.objects.get(id=item_id)
            item.reserved += payment.quantity
            item.supply -= payment.quantity
            item.save()

        order.get_required_amount()
        order.fix_rates()

        response_data = {"id": order.id}
        if currency == 'paypal':
            process_correct_payment(order)
        return Response(response_data, status=status.HTTP_200_OK)


class CheckActive(APIView):
    '''
    Checking user's payment status.
    Polling by frontend for cart reset.
    '''
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


def check_paypal(paypal_id):
    try:
        paypal_payment = GetOrder().get_order(paypal_id)
        print(paypal_payment.__dict__)
    except Exception as e:
        print(e)
        return {'error': 'could not get info from paypal'}
    status = paypal_payment.result.status
    print(status)
    correct_date = paypal_payment.result.create_time
    date = datetime.datetime.strptime(correct_date.replace('T', '-').replace('Z', ''), '%Y-%m-%d-%H:%M:%S')
    print(date)
    merchant = paypal_payment.result.purchase_units[0]['payee']['merchant_id']
    print(merchant)
    if status in ('COMPLETED', 'APPROVED') and merchant == 'ECMHZAXMARXAW' and (datetime.datetime.now() - date) < datetime.timedelta(hours=4):
        return True
    else:
        return {'error': 'invalid paypal payment'}