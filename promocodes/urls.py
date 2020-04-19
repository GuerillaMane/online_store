from django.urls import path, include
from django.conf.urls import url
from .views import (
    PromoList,
    PromoCreate,
    PromoDelete,
    PromoDetail,
    PromoUpdate,
    promocode_apply
)

app_name = 'promocodes'


urlpatterns = [
    url(r'^apply/$', promocode_apply, name='apply_code'),
    path('api/', include('promocodes.api.urls')),
    path('list/', PromoList.as_view(), name='promo_list'),
    path('info/<int:pk>/', PromoDetail.as_view(), name='promo_detail'),
    path('create/', PromoCreate.as_view(), name='promo_create'),
    path('update/<int:pk>/', PromoUpdate.as_view(), name='promo_update'),
    path('delete/<int:pk>/', PromoDelete.as_view(), name='promo_delete'),
]
