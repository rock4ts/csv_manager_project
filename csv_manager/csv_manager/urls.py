from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('csv_api/', include('api.urls')),
]

schema_view = get_schema_view(
   openapi.Info(
      title="CSV-manager API",
      default_version='v1',
      description="Документация для приложения file_data проекта CSV-manager",
      contact=openapi.Contact(email="rock4ts@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   re_path(r'^redoc/$',
           schema_view.with_ui('redoc', cache_timeout=0),
           name='schema-redoc'),
]
