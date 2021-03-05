from django.core.management.base import BaseCommand, CommandError
from remusgold.withdraw.api import withdraw_funds

if __name__ == '__main__':
    print('Started withdrawing funds', flush=True)
    withdraw_funds()
    print('Withdraw completed', flush=True)


class Command(BaseCommand):
    help = 'Withdraw funds from internal accounts'

    def handle(self, *args, **options):
        print('Started withdrawing funds', flush=True)
        try:
            withdraw_funds()
        except Exception as e:
            print('Withdraw produced error. Stopping. Error is:', flush=True)
            print(e, flush=True)

        print('Withdraw completed', flush=True)