from django.urls import path
from remusgold.account.views import RegisterView, GetView, ShippingView, BillingView
from rest_framework.authtoken import views


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('<str:token>/', GetView.as_view()),
    #path('login/', views.ObtainAuthToken.as_view()),
    #path('login2/', views.obtain_auth_token),
    path('<str:token>/shipping/', ShippingView.as_view()),
    path('<str:token>/billing/', BillingView.as_view())
]