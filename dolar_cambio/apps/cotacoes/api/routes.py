from django.urls import include, path
from rest_framework import routers

from cotacoes.api.viewsets import AtualizarCotacoesViewSet, CotacaoViewSet

router = routers.DefaultRouter()
router.register("cotacoes", CotacaoViewSet, basename="cotacao")

urlpatterns = [
    path("", include(router.urls)),
    path("atualizar-cotacoes/", AtualizarCotacoesViewSet.as_view(), name="atualizar"),
]
