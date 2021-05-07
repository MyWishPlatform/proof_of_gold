import os
import sys
import time
import json
import requests
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remusgold.settings')
import django

django.setup()

from remusgold.rates.models import UsdRate
from remusgold.settings import GOLD_CHECKER_TIMEOUT, GOLD_CHECKER_API_KEY, GOLD_OUNCE
from remusgold.store.models import Item

API_URL = 'https://metals-api.com/api/latest?access_key={api_key}'

def get_rates():
    res = requests.get(API_URL.format(api_key=GOLD_CHECKER_API_KEY))
    if res.status_code != 200:
        raise Exception('cannot get exchange rate for XAU')
    answer = json.loads(res.text)

    return answer


if __name__ == '__main__':
    while True:
        try:
            metal_rates = get_rates()
        except Exception as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)
            time.sleep(GOLD_CHECKER_TIMEOUT)
            continue

        print('new metal prices', metal_rates, flush=True)
        if metal_rates['success']:
            try:
                rate_object = UsdRate.objects.get(currency='XAU')
            except UsdRate.DoesNotExist:
                rate_object = UsdRate(currency='XAU')

            rate_object.rate = 1 / metal_rates['rates']['XAU'] / GOLD_OUNCE
            rate_object.save()

        for item in Item.objects.all():
            result = item.update_price()
            print(result)

        time.sleep(GOLD_CHECKER_TIMEOUT)
