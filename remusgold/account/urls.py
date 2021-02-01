from django.urls import path
from django.conf.urls import url
from remusgold.account.views import RegisterView, GetView, ShippingView, BillingView, ObtainAuthTokenWithId
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('<str:token>/', GetView.as_view()),
    path('api-token-auth/', ObtainAuthTokenWithId.as_view()),
    url(r'^login/$', views.ObtainAuthToken.as_view(), name='login'),
    path('<str:token>/shipping/', ShippingView.as_view()),
    path('<str:token>/billing/', BillingView.as_view())
]