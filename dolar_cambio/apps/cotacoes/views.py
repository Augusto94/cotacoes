from datetime import datetime
from typing import Dict

import pandas as pd
from django.views.generic import TemplateView

from cotacoes.models import Cotacao


class CotacoesView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs) -> Dict:
        """Retorna o contexto para renderizar o gŕafico na página de cotações.

        Retorna um dicionário com as informações das cotações a serem exibidas na página
        e as datas de início e fim selecionadas pelo usuário ou as datas padrão.

        Returns:
            Dict: Dicionário contendo as informações das cotações e datas selecionadas.
        """
        context = super().get_context_data(**kwargs)

        # Verifica se os parâmetros de data foram fornecidos na URL
        data_inicio_str = self.request.GET.get("data_inicio")
        data_fim_str = self.request.GET.get("data_fim")

        # Obtém a data da cotação mais recente no banco
        data_atual = Cotacao.objects.order_by("-data").values_list("data", flat=True).first().date()

        # Calcula a data 5 dias úteis atrás em relação à data atual
        cinco_dias_uteis_atras = pd.date_range(end=data_atual, periods=5, freq="B")[0].date()

        # Converte as strings em objetos de data se fornecidos, caso contrário, usa as datas padrão
        data_inicio = (
            datetime.strptime(data_inicio_str, "%Y-%m-%d").date()
            if data_inicio_str
            else cinco_dias_uteis_atras
        )
        data_fim = (
            datetime.strptime(data_fim_str, "%Y-%m-%d").date() if data_fim_str else data_atual
        )

        cotacoes = Cotacao.objects.filter(data__gte=data_inicio, data__lte=data_fim).order_by(
            "data"
        )

        context.update(
            {
                "dados_cotacao": [
                    {
                        "moeda": cotacao.moeda,
                        "data": str(cotacao.data.date()),
                        "valor": cotacao.valor,
                    }
                    for cotacao in cotacoes
                ],
                "data_inicio": data_inicio.strftime("%Y-%m-%d %H:%M:%S"),
                "data_fim": data_fim.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        return context
