from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from remusgold.vouchers.models import Voucher
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from remusgold.consts import DECIMALS

activation_success_response = openapi.Response(
    description='response with transaction hash if token transfer was successful',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'tx_hash': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)

activation_fail_response = openapi.Response(
    description='voucher activation fail cause: `USED`, `EXPIRED` or `TRANSFER FAIL`',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'detail': openapi.Schema(type=openapi.TYPE_STRING)
        },
    )
)

not_found_response = openapi.Response(
    description='response if no such voucher exists',
)

@method_decorator(csrf_exempt, name='dispatch')
class VoucherActivationView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'activation_code': openapi.Schema(type=openapi.TYPE_STRING),
                'duc_address': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['activation_code', 'ducx_address']
        ),
        responses={200: activation_success_response, 403: activation_fail_response, 404: not_found_response},
    )
    def post(self, request):
        request_data = request.data
        activation_code = request_data['activation_code']
        duc_address = request_data['duc_address']

        print(f'VOUCHER ACTIVATION: received activation code {activation_code} from {duc_address}', flush=True)
        try:
            voucher = Voucher.objects.get(activation_code=activation_code)
        except ObjectDoesNotExist:
            print(f'VOUCHER ACTIVATION: voucher {activation_code} doesn`t exist', flush=True)
            return Response(status=404)

        if voucher.is_used:
            print(f'VOUCHER ACTIVATION: voucher {activation_code} has already been used', flush=True)
            return Response({'detail': 'USED'}, status=403)
        transfer = voucher.activate(duc_address)
        voucher.save()
        token_amount = transfer.amount / DECIMALS['DUC']
        if transfer.tx_hash:
            print(f'VOUCHER ACTIVATION: Successful transfer {transfer.tx_hash} to {transfer.duc_address} '
                  f'for {token_amount} {transfer.currency}', flush=True)
            return Response({'tx_hash': transfer.tx_hash, 'usd_amount': voucher.usd_amount,
                             'duc_amount': token_amount, 'lock_days': 0}, status=200)
        else:
            print(f'VOUCHER ACTIVATION: Failed transfer {token_amount} {transfer.currency} to {transfer.duc_address} '
                  f'with exception {transfer.tx_error}', flush=True)
            return Response({'detail': 'TRANSFER FAIL'}, status=403)