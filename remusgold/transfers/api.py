from remusgold.transfers.models import Transfer
import json
import requests
from django.utils import timezone
from decimal import Decimal
from remusgold.litecoin_rpc import DucatuscoreInterface, DucatuscoreInterfaceException
from rest_framework.exceptions import PermissionDenied, APIException
from remusgold.settings import RATES_API_URL
from remusgold.consts import DECIMALS

def duc_transfer(duc_address, duc_amount):
    try:
        rpc = DucatuscoreInterface()
        tx_hash = rpc.node_transfer(duc_address, duc_amount)
    except DucatuscoreInterfaceException as err:
        transfer.transfer_status = 'ERROR'
        transfer.save()
        raise APIException(detail=str(err))

    return tx_hash


def confirm_transfer(message):
    tx_hash = message.get('txHash')
    transfer = Transfer.objects.get(tx_hash=tx_hash)
    transfer.transfer_status = 'CONFIRMED'
    transfer.save()