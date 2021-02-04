from django.urls import path
from remusgold.account.views import RegisterView, GetView, ShippingView, BillingView, ObtainAuthTokenWithId, register_activate, ResetView
from rest_framework.authtoken import views


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('<str:token>/', GetView.as_view()),
    path('password_reset', ResetView.as_view()),
    path('login', ObtainAuthTokenWithId.as_view()),
    path('<str:token>/shipping/', ShippingView.as_view()),
    path('<str:token>/billing/', BillingView.as_view()),
    path('register/activate/<str:sign>', register_activate)
]