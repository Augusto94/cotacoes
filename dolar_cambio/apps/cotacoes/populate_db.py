import logging
from datetime import date, datetime, timedelta
from typing import Dict, List

import pytz
import requests

from cotacoes.models import Cotacao

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def gerar_datas() -> List[datetime]:
    """Gera uma lista de datas a partir da última data no banco de dados até a data atual.

    Returns:
        List[datetime]: Uma lista de objetos datetime representando as datas.
    """
    ultima_data_banco = Cotacao.objects.order_by("-data").values_list("data", flat=True).first()
    if ultima_data_banco:
        data_inicial = (ultima_data_banco + timedelta(1)).date()
    else:
        data_inicial = datetime.strptime("1999-01-04", "%Y-%m-%d").date()

    data_atual = date.today()
    dias_diff = (data_atual - data_inicial).days

    return [data_atual - timedelta(i) for i in range(dias_diff + 1)]


def get_cotacoes_json(date: datetime) -> Dict:
    """Obtém as cotações para uma data específica.

    Args:
        date (datetime): A data para obter as cotações.

    Returns:
        Dict: Dados da cotação obtidos na API em formato JSON.
    """
    response = requests.get(f"https://api.vatcomply.com/rates?base=USD&date={str(date)}")
    return response.json()


def criar_cotacoes(json_data: Dict) -> None:
    """Cria os objetos Cotacao no banco de dados a partir dos dados obtidos na API.

    Args:
        json_data (Dict): Dados da cotação obtidos na API.
    """
    data_cotacao = datetime.strptime(json_data.get("date"), "%Y-%m-%d")
    data_cotacao = pytz.timezone("America/Recife").localize(data_cotacao)
    Cotacao.objects.bulk_create(
        [
            Cotacao(
                moeda="Real",
                sigla="BRL",
                data=data_cotacao,
                valor=json_data.get("rates", {}).get("BRL"),
            ),
            Cotacao(
                moeda="Euro",
                sigla="EUR",
                data=data_cotacao,
                valor=json_data.get("rates", {}).get("EUR"),
            ),
            Cotacao(
                moeda="Iene",
                sigla="JPY",
                data=data_cotacao,
                valor=json_data.get("rates", {}).get("JPY"),
            ),
        ]
    )
    logger.info(f"Cotações criadas para data {json_data.get('date')}")


def popular_banco() -> None:
    """Popula o banco de dados com as cotações obtidas da API para várias datas."""
    datas_list = gerar_datas()
    for data in datas_list:
        cotacoes_json = get_cotacoes_json(data)
        if cotacoes_json.get("date") == str(data):
            criar_cotacoes(cotacoes_json)
