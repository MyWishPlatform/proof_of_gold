from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from remusgold.consts import DECIMALS
from remusgold.quantum.models import Charge
from remusgold.quantum.api import initiate_charge


class ChargeSerializer(serializers.ModelSerializer):
    currencies = ['USD', 'EUR', 'GBP', 'CHF']

    class Meta:
        model = Charge
        fields = ['amount', 'currency', 'email']

    def create(self, validated_data):
        amount = validated_data['amount']
        currency = validated_data['currency']
        email = validated_data['email']

        raw_amount = amount / DECIMALS[currency]
        charge_info = initiate_charge(currency, raw_amount, email)

        validated_data = {
            'charge_id': charge_info['id'],
            'status': charge_info['status'],
            'currency': currency,
            'amount': amount,
            'hash': charge_info['hash'],
            'redirect_url': charge_info['url'],
            'email': email,
        }

        return super().create(validated_data)

    def validate_currency(self, value):
        if value not in self.currencies:
            raise ValidationError(detail=f'currency must be in {self.currencies}')
        return value

    def validate_amount(self, value):
        # Validating all fiat with same decimals
        if value < 1 * DECIMALS['USD']:
            raise ValidationError(detail=f'amount must be greater or equal then 1')
        return value
