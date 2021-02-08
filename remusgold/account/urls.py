from django.urls import path
from django.conf.urls import url
from remusgold.account.views import RegisterView, GetView, ShippingView, BillingView, ObtainAuthTokenWithId, \
register_activate, reset_password_request_token, reset_password_validate_token, GetAddressesView, check_code
from rest_framework.authtoken import views

from django_rest_resetpassword.views import reset_password_confirm

app_name = 'reset_password'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('checkout_addresses/<str:token>', GetAddressesView.as_view()),
    path('<str:token>/', GetView.as_view()),
    path('reset/validate_token/<str:token>/', reset_password_validate_token, name="reset-password-validate"),
    url(r'^reset/confirm/', reset_password_confirm, name="reset-password-confirm"),
    url(r'^reset', reset_password_request_token, name="reset-password-request"),
    path('login/check_code', check_code),
    path('login', ObtainAuthTokenWithId.as_view()),
    path('<str:token>/shipping/', ShippingView.as_view()),
    path('<str:token>/billing/', BillingView.as_view()),
    path('register/activate/<str:sign>', register_activate)
]
