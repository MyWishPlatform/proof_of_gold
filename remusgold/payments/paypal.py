from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest

from remusgold.settings_local import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_TESTNET

import sys


class PayPalClient:
    def __init__(self):
        self.client_id = PAYPAL_CLIENT_ID
        self.client_secret = PAYPAL_CLIENT_SECRET

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        if PAYPAL_TESTNET:
            self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        else:
            self.environment = LiveEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
                self.object_to_json(value) if not self.is_primittive(value) else \
                    value
        return result;

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item) \
                                  else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result;

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)


class GetOrder(PayPalClient):
    # 2. Set up your server to receive a call from the client
    """You can use this function to retrieve an order by passing order ID as an argument"""

    def get_order(self, order_id):
        """Method to get order"""
        request = OrdersGetRequest(order_id)
        # 3. Call PayPal to get the transaction
        response = self.client.execute(request)
        # 4. Save the transaction in your database. Implement logic to save transaction to your database for future reference.
        return response

if __name__ == '__main__':
    response = GetOrder().get_order('4XW394256V238001T')