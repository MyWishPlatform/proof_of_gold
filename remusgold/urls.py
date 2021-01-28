"""remusgold URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from rest_framework import status
from rest_framework import permissions
from remusgold.settings import MEDIA_URL, MEDIA_ROOT, STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="remusgold",
        default_version='v1',
        description="API for remusgold store",
        contact=openapi.Contact(email="ephdtrg@mintyclouds.in"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/store/', include('remusgold.store.urls')),
    path('api/v1/payments/', include('remusgold.payments.urls')),
    path('api/v1/account/', include('remusgold.account.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
