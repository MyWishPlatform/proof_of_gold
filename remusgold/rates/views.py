from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from remusgold.rates.api import get_usd_prices


rates_response = openapi.Response(
    description='ETH, BTC, USDC rates',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'ETH': openapi.Schema(type=openapi.TYPE_STRING),
            'BTC': openapi.Schema(type=openapi.TYPE_STRING),
            'USDC': openapi.Schema(type=openapi.TYPE_STRING)
            },
    )
)


class RateRequest(APIView):
    @swagger_auto_schema(
        operation_description="rate request",
        responses={200: rates_response}
    )
    def get(self, request):
        usd_price = get_usd_prices()
        response_data = {currency: price for currency, price in usd_price.items()}
        return Response(response_data, status=status.HTTP_200_OK)