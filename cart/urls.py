from django.urls import path
from django.conf.urls import url
from .views import (
    cart_add,
    cart_remove,
    cart_detail,
    cart_error
)


app_name = 'cart'


urlpatterns = [
    url(r'^$', cart_detail, name='cart_detail'),
    url(r'^add/(?P<item_id>\d+)/$', cart_add, name='cart_add'),
    url(r'^remove/(?P<item_id>\d+)/$', cart_remove, name='cart_remove'),
    path('error/', cart_error, name='cart_error')
]
