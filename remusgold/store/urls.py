from django.urls import path
from remusgold.store.views import GroupView, StoreView, UniqueView, ReviewView, SearchView, contact_us

urlpatterns = [
    path('<int:id>/', UniqueView.as_view()),
    path('<str:group>/', GroupView.as_view()),
    path('review', ReviewView.as_view()),
    path('search', SearchView.as_view()),
    path('', StoreView.as_view()),
    path('contact_us', contact_us),
]