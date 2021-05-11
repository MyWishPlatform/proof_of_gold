from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken import views
from django_rest_resetpassword.views import reset_password_confirm

from remusgold.account.views import RegisterView, GetView, ShippingView, BillingView, ObtainAuthTokenWithId, \
    register_activate, reset_password_request_token, reset_password_validate_token, GetAddressesView, check_code, \
    total_id_count, get_or_create_referral_code

app_name = 'reset_password'

urlpatterns = [
    path('register/<str:ref_code>', RegisterView.as_view()),
    path('register/', RegisterView.as_view()),
    path('checkout_addresses/<str:token>', GetAddressesView.as_view()),
    path('total/', total_id_count),
    path('<str:token>/referral_code/', get_or_create_referral_code),
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
