from django.urls import path
from remusgold.store.views import GroupView, StoreView, UniqueView, ReviewView

urlpatterns = [
    path('<int:id>/', UniqueView.as_view()),
    path('<str:group>/', GroupView.as_view()),
    path('review/' ReviewView.as_view()),
    path('', StoreView.as_view())
]