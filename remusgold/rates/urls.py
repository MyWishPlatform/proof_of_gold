from django.urls import path
from remusgold.rates.views import RateRequest
urlpatterns = [
    path('', RateRequest.as_view()),
]