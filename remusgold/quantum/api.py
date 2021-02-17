import json
import requests
import datetime
from django.utils import timezone

from remusgold.quantum.models import QuantumAccount
from remusgold.settings import QUANTUM_CLIENT_ID, QUANTUM_CLIENT_SECRET, QUANTUM_API_URL, QUANTUM_REDIRECT_URL


class QuantumApiError(Exception):
    pass


def initiate_charge(currency, amount, email):
    quantum_account = QuantumAccount.objects.first()
    update_access_token(quantum_account)

    new_charge_data = {
        'amount': {
            'currencyCode': currency,
            'value': amount,
        },
        'email': email,
        'tokenCurrencyCode': f'Q{currency}',
        'receivingAccountAddress': quantum_account.address,
        'returnUrl': QUANTUM_REDIRECT_URL,
    }

    headers = {
        'Authorization': '{token_type} {access_token}'.format(token_type=quantum_account.token_type,
                                                              access_token=quantum_account.access_token)
    }

    try:
        creation_request = requests.post(QUANTUM_API_URL.format('api/v1/merchant/charges'),
                                         json=new_charge_data,
                                         headers=headers)
    except Exception:
        raise QuantumApiError

    return json.loads(creation_request.content)


def update_access_token(quantum_account: QuantumAccount):
    token_expires_at = quantum_account.token_expires_at or 0
    token_expiration_delta = token_expires_at + datetime.timedelta(minutes=5).seconds
    if not quantum_account.access_token or token_expiration_delta < timezone.now().timestamp():
        request_data = {
            'client_id': QUANTUM_CLIENT_ID,
            'client_secret': QUANTUM_CLIENT_SECRET,
            'grant_type': 'client_credentials',
        }
        new_token_request = requests.post(QUANTUM_API_URL.format('connect/token'), data=request_data)
        token_info = json.loads(new_token_request.content)

        quantum_account.token_type = token_info['token_type']
        quantum_account.access_token = token_info['access_token']
        quantum_account.token_expires_at = timezone.now().timestamp() + token_info['expires_in']
        quantum_account.save()
