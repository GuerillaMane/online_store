from django.conf.urls import url, include
from django.urls import path
from . import views

app_name = 'order_app'


urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    path('api/', include('order_app.api.urls')),
    path('error/', views.order_error, name='order_error')
]
