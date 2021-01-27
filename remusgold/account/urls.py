from django.urls import path
from remusgold.account.views import RegisterView, GetView, ShippingView, BillingView
from rest_framework.authtoken import views


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('<int:id>/', GetView.as_view()),
    path('login/', views.obtain_auth_token),
    path('<int:id>/shipping/', ShippingView.as_view()),
    path('<int:id>/billing/', BillingView.as_view())
]