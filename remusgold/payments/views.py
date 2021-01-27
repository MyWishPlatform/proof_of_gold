from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.decorators import api_view

from remusgold.payments.models import Payment
from remusgold.store.models import Item
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
        payments = Payment.objects.filter(user_id=user_id)

        for payment in payments:
            item = payment.item
            payment_list.append({'created_date': payment.created_date, 'item_id': item.id, 'item_name': item.name,
                                 'item_image': item.images.path, 'quantity': payment.quantity, 'created_date': payment.created_date})
        response_data = {
            'payments': payment_list,
        }
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
        response_data = {'created_date': payment.created_date, 'item_id': item.id, 'item_name': item.name,
            'item_image': ALLOWED_HOSTS[0] + item.images.url, 'quantity': payment.quantity, 'created_date': payment.created_date}
        print('res:', response_data)

        return Response(response_data, status=status.HTTP_200_OK)


class CreatePaymentView(APIView):

    @swagger_auto_schema(
        operation_description="get single user's payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['quantity', 'user_id', 'item'],
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_NUMBER),
                'user_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                'item_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ),
        responses={200: 'OK'},
    )
    def post(self, request):
        request_data = request.data
        item_id = request_data.get('item_id')
        user_id = request_data.get('user_id')
        quantity = request_data.get('quantity')
        payment = Payment(user_id=user_id, item_id=item_id, quantity=quantity)
        payment.save()
        item = Item.objects.get(id=payment.item_id)
        item.sold += quantity
        item.supply -= quantity
        item.save()

        return Response('OK', status=status.HTTP_200_OK)