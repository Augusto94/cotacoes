from datetime import datetime

from django.test import RequestFactory, TestCase
from django.urls import reverse

from cotacoes.models import Cotacao
from cotacoes.views import CotacoesView


class CotacoesViewTestCase(TestCase):
    def setUp(self):
        # Cria algumas instâncias de Cotacao para testar a view
        Cotacao.objects.create(
            moeda="Iene", valor=141.0147801009373, data="2023-07-24T00:00:00-03:00"
        )
        Cotacao.objects.create(
            moeda="Euro", valor=0.9012256669069936, data="2023-07-24T00:00:00-03:00"
        )
        Cotacao.objects.create(
            moeda="Real", valor=4.774783705839942, data="2023-07-24T00:00:00-03:00"
        )

    def test_get_context_data_default_dates(self):
        # Testa o comportamento padrão da view quando não há parâmetros de data fornecidos na URL
        url = reverse("cotacoes_view")
        request = RequestFactory().get(url)
        response = CotacoesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.context_data.get("dados_cotacao")
        )  # Verifica se a chave 'dados_cotacao' existe no contexto
        self.assertTrue(
            response.context_data.get("data_inicio")
        )  # Verifica se a chave 'data_inicio' existe no contexto
        self.assertTrue(
            response.context_data.get("data_fim")
        )  # Verifica se a chave 'data_fim' existe no contexto

        # Verifica se a quantidade de dados de cotação no contexto é igual ao número de instâncias criadas
        cotacoes = Cotacao.objects.all()
        self.assertEqual(len(response.context_data["dados_cotacao"]), cotacoes.count())

    def test_get_context_data_custom_dates(self):
        # Testa o comportamento da view quando são fornecidos parâmetros de data na URL
        url = reverse("cotacoes_view")
        data_inicio = "2023-07-21"
        data_fim = "2023-07-24"
        request = RequestFactory().get(url, {"data_inicio": data_inicio, "data_fim": data_fim})
        response = CotacoesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.context_data.get("dados_cotacao")
        )  # Verifica se a chave 'dados_cotacao' existe no contexto
        self.assertTrue(
            response.context_data.get("data_inicio")
        )  # Verifica se a chave 'data_inicio' existe no contexto
        self.assertTrue(
            response.context_data.get("data_fim")
        )  # Verifica se a chave 'data_fim' existe no contexto

        # Verifica se a quantidade de dados de cotação no contexto é correta de acordo com as datas fornecidas
        data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()
        cotacoes = Cotacao.objects.filter(data__gte=data_inicio_obj, data__lte=data_fim_obj)
        self.assertEqual(len(response.context_data["dados_cotacao"]), cotacoes.count())

    def test_get_context_data_invalid_dates(self):
        # Testa o comportamento da view quando são fornecidos parâmetros de data inválidos na URL
        url = reverse("cotacoes_view")
        data_inicio = "2023-07-30"  # Data posterior à data mais recente no banco
        data_fim = "2023-07-21"  # Data anterior à data mais antiga no banco
        request = RequestFactory().get(url, {"data_inicio": data_inicio, "data_fim": data_fim})
        response = CotacoesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            response.context_data.get("dados_cotacao")
        )  # Verifica se a chave 'dados_cotacao' existe no contexto
        self.assertTrue(
            response.context_data.get("data_inicio")
        )  # Verifica se a chave 'data_inicio' existe no contexto
        self.assertTrue(
            response.context_data.get("data_fim")
        )  # Verifica se a chave 'data_fim' existe no contexto

        # Verifica se a quantidade de dados de cotação no contexto é 0, pois as datas são inválidas
        self.assertEqual(len(response.context_data["dados_cotacao"]), 0)

    def test_get_context_data_no_cotacoes(self):
        # Testa o comportamento da view quando não há cotacoes no banco de dados
        Cotacao.objects.all().delete()
        url = reverse("cotacoes_view")
        request = RequestFactory().get(url)
        response = CotacoesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            response.context_data.get("dados_cotacao")
        )  # Verifica se a chave 'dados_cotacao' existe no contexto
        self.assertTrue(
            response.context_data.get("data_inicio")
        )  # Verifica se a chave 'data_inicio' existe no contexto
        self.assertTrue(
            response.context_data.get("data_fim")
        )  # Verifica se a chave 'data_fim' existe no contexto

        # Verifica se a quantidade de dados de cotação no contexto é 0, pois não há cotacoes no banco
        self.assertEqual(len(response.context_data["dados_cotacao"]), 0)
