from django.urls import path, include
from django.conf.urls import url
from .views import promocode_apply

app_name = 'promocodes'


urlpatterns = [
    url(r'^apply/$', promocode_apply, name='apply_code'),
    path('api/', include('promocodes.api.urls')),
]
