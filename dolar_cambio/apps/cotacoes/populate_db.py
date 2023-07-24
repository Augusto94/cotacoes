import asyncio
from datetime import date, datetime, timedelta

import aiohttp
import pytz
from asgiref.sync import sync_to_async

from cotacoes.models import Cotacao
from cotacoes.utils import chunks


async def gerar_datas():
    data_inicial = datetime.strptime("1999-01-04", "%Y-%m-%d")
    data_atual = datetime.strptime(str(date.today()), "%Y-%m-%d")
    dias_diff = (data_atual - data_inicial).days

    return [data_atual - timedelta(i) for i in range(dias_diff + 1)]


async def get_cotacoes(date):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://api.vatcomply.com/rates?base=USD&date={str(date.date())}"
        ) as response:
            response = await response.json()
            if response.get("date") and response.get("date") in str(date):
                await create_cotacoes(response)


@sync_to_async
def create_cotacoes(json_data):
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
    print(f"Cotações criadas para data {json_data.get('date')}")


async def popular_banco():
    datas_list = await gerar_datas()
    for datas_chunk in chunks(datas_list, 50):
        await asyncio.gather(*[get_cotacoes(data) for data in datas_chunk])


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(popular_banco())
    loop.close()
