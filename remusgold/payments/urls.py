from django.urls import path
from remusgold.payments.views import GetPaymentsView, GetSinglePaymentView, CreatePaymentView

urlpatterns = [
    path('<int:payment_id>/', GetSinglePaymentView.as_view()),
    path('user/<str:token>', GetPaymentsView.as_view()),
    path('<str:token>/', CreatePaymentView.as_view()),
]