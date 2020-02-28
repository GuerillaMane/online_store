from django.urls import path, include
from .views import (
    IndexView,
    ItemListView,
)


app_name = 'shop'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('item_list/', ItemListView.as_view(), name='item_list'),
]
