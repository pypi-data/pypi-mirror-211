# coding=utf-8
""" Register builtin url's here. """
from django.urls import (
    include,
    re_path,
)

from .views import schema_view

urlpatterns = [
    re_path(r'^$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^api-auth/', include('rest_framework.urls'))
]
