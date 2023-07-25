from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cotacoes.api.serializers import CotacaoSerializer
from cotacoes.models import Cotacao


class CotacaoAPITestCase(APITestCase):
    def setUp(self):
        # Cria instâncias de Cotacao para testar a listagem
        Cotacao.objects.create(
            moeda="Iene", sigla="JPY", valor=141.0147801009373, data="2023-07-24T00:00:00-03:00"
        )
        Cotacao.objects.create(
            moeda="Euro", sigla="EUR", valor=0.9012256669069936, data="2023-07-24T00:00:00-03:00"
        )
        Cotacao.objects.create(
            moeda="Real", sigla="BRL", valor=4.774783705839942, data="2023-07-24T00:00:00-03:00"
        )

    def test_list_cotacoes(self):
        # Faz uma requisição GET para a rota de listagem de cotacoes
        url = reverse("cotacao-list")
        response = self.client.get(url)

        # Verifica se o status code é 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica se a contagem de resultados é igual ao número de instâncias criadas
        self.assertEqual(len(response.data["results"]), 3)

        # Verifica se a resposta é igual ao serializer das instâncias criadas
        cotacoes = Cotacao.objects.all()
        serializer = CotacaoSerializer(cotacoes, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_cotacoes_empty(self):
        # Testa a listagem quando não há cotacoes no banco de dados
        Cotacao.objects.all().delete()
        url = reverse("cotacao-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
