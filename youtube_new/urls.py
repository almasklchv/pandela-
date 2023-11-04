from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Pandela API",
      default_version='v1',
      description="По сути auth - вход, выход, регистрация(но это вообще чисто мини-веточка от account так-то. вся инфа в account), account - вся инфа об аккаунте, ужее сам профиль и его оформление и также инфа, идущая в auth, blogs - видосики. чтоб нее путался: ",
      terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   # permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("api/profile/", include("profiles.urls")),
    path("api/auth/", include("auth.urls")),
    path('api/blogs/', include('blogs.urls')),
]
