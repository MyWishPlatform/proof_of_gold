from django.urls import path
from remusgold.payments.views import GetPaymentsView, GetSinglePaymentView, CreatePaymentView

urlpatterns = [
    path('<int:payment_id>/', GetSinglePaymentView.as_view()),
    path('user/<int:user_id>', GetPaymentsView.as_view()),
    path('', CreatePaymentView.as_view()),
]