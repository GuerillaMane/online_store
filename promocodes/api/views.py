from rest_framework.viewsets import ModelViewSet
from .serializers import PromoCodeSerializer
from ..models import PromoCode


class PromoCodeViewSet(ModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
