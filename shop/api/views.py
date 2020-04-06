from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ItemSerializer,
    ShopSerializer,
    CategorySerializer,
)
from ..models import (
    Item,
    Shop,
    Category,
)


class CategoryViewSet(ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(is_delete=False)
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def all_instances(self, request, *args, **kwargs):
        queryset = Category.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
