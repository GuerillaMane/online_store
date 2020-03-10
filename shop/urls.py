from django.urls import path, include
from django.conf.urls import url
from .views import (
    IndexView,
    ItemListView,
    ItemCreate,
    ItemDelete,
    ItemUpdate,
    item_detail,
    item_list,
)

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('item_list/', ItemListView.as_view(), name='item_list'),
    path('item_create/', ItemCreate.as_view(), name='item_create'),
    path('item_update/<int:pk>/', ItemUpdate.as_view(), name='item_update'),
    path('item_delete/<int:pk>/', ItemDelete.as_view(), name='item_delete'),
    # url(r'^$', item_list, name='item_list'),
    # url(r'^(?P<category_slug>[-\w]+)/$', item_list, name='item_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', item_detail, name='item_detail')
]
