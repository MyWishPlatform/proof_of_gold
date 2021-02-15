from remusgold.rates.models import UsdRate
from remusgold.consts import SUPPORTED_CURRENCIES
from remusgold.consts import DECIMALS


def get_usd_prices():
    usd_prices = {currency: UsdRate.objects.get(currency=currency).rate for currency in SUPPORTED_CURRENCIES}
    print('current rates', usd_prices, flush=True)

    return usd_prices


def calculate_amount(original_amount, from_currency, to_currency):
    print('Calculating amount, original: {orig}, from {from_curr} to {to_curr}'.format(
        orig=original_amount,
        from_curr=from_currency,
        to_curr=to_currency),
        flush=True)

    usd_rates = get_usd_prices()

    currency_rate = usd_rates[from_currency] / usd_rates[to_currency]
    amount = int(int(original_amount / DECIMALS[from_currency] * DECIMALS[to_currency]) * currency_rate)

    return amount, currency_rate
