from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from cotacoes.models import Cotacao
from cotacoes.populate_db import popular_banco

from .serializers import CotacaoSerializer


class CotacaoViewSet(ModelViewSet):
    serializer_class = CotacaoSerializer
    queryset = Cotacao.objects.order_by("-data")
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "data",
        "moeda",
        "sigla",
    ]


class AtualizarCotacoesViewSet(APIView):
    def get(self, request):
        popular_banco()
        return Response({"message": "Cotações capturadas com sucesso!"})
