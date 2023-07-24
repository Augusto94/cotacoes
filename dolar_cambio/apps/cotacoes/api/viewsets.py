from rest_framework.viewsets import ModelViewSet

from cotacoes.models import Cotacao

from .serializers import CotacaoSerializer


class CotacaoViewSet(ModelViewSet):
    serializer_class = CotacaoSerializer
    queryset = Cotacao.objects.order_by("-data")
