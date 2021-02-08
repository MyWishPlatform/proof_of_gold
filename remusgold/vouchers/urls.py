from django.urls import path
from remusgold.vouchers.views import VoucherActivationView

urlpatterns = [
    path('activate/', VoucherActivationView.as_view()),
]