from datetime import datetime
from typing import Dict

import pandas as pd
from dateparser import parse as parse_date
from django.contrib import messages
from django.views.generic import TemplateView

from cotacoes.models import Cotacao


class CotacoesView(TemplateView):
    template_name = "grafico.html"

    def get_context_data(self, **kwargs) -> Dict:
        """Retorna o contexto para renderizar o gŕafico na página de cotações.

        Retorna um dicionário com as informações das cotações a serem exibidas na página
        e as datas de início e fim selecionadas pelo usuário ou as datas padrão.

        Returns:
            Dict: Dicionário contendo as informações das cotações e datas selecionadas.
        """
        context = super().get_context_data(**kwargs)

        # Verifica se os parâmetros de data foram fornecidos na URL
        data_inicio_str = self.request.GET.get("data_inicio", "")
        data_fim_str = self.request.GET.get("data_fim", "")

        data_inicio = parse_date(data_inicio_str)
        data_fim = parse_date(data_fim_str)

        # Verifica se datas fornecidas possuem um intervalo válido
        if data_inicio:
            data_inicio = data_inicio.date()
            data_fim = data_fim.date()
            if str(data_inicio) <= str(pd.date_range(end=data_fim, periods=6, freq="B")[0].date()):
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    f"Intervalo de datas ({data_inicio_str} -> {data_fim_str}) é maior do que 5 dias úteis.",
                )
                data_inicio = None
                data_fim = None

        # Obtém a data da cotação mais recente no banco
        data_atual = Cotacao.objects.order_by("-data").values_list("data", flat=True).first()
        data_atual = data_atual.date() if data_atual else datetime.now().date()

        # Calcula a data 5 dias úteis atrás em relação à data atual
        cinco_dias_uteis_atras = pd.date_range(end=data_atual, periods=5, freq="B")[0].date()

        # Usa as datas fornecidas se houver, caso contrário, usa as datas padrão
        data_inicio = data_inicio if data_inicio else cinco_dias_uteis_atras
        data_fim = data_fim if data_fim else data_atual

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
