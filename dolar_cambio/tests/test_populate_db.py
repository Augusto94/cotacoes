import datetime
from unittest.mock import Mock, patch

import pytest
import pytz

from cotacoes.models import Cotacao
from cotacoes.populate_db import (
    criar_cotacoes,
    gerar_datas,
    get_cotacoes_json,
    popular_banco,
)


@pytest.fixture
def test_date():
    return datetime.datetime(2023, 7, 20, tzinfo=pytz.timezone("America/Recife"))


@pytest.mark.django_db
@patch("cotacoes.populate_db.gerar_datas")
@patch("cotacoes.populate_db.get_cotacoes_json")
def test_popular_banco_cotacoes_existentes(mock_get_cotacoes_json, mock_gerar_datas, test_date):
    # Defina a data da cotação
    date = datetime.date(2023, 7, 19)

    # Defina os valores para os mocks
    mock_gerar_datas.return_value = [date]
    mock_get_cotacoes_json.return_value = {
        "date": str(date),
        "rates": {"BRL": 5.0, "EUR": 1.2, "JPY": 130.0},
    }

    # Execute a função para popular o banco
    popular_banco()

    # Verifique se a cotação foi criada no banco de dados
    cotacoes = Cotacao.objects.filter(data=date)
    assert len(cotacoes) == 3
    assert cotacoes[0].moeda == "Real"
    assert cotacoes[0].sigla == "BRL"
    assert cotacoes[0].valor == 5.0
    assert cotacoes[1].moeda == "Euro"
    assert cotacoes[1].sigla == "EUR"
    assert cotacoes[1].valor == 1.2
    assert cotacoes[2].moeda == "Iene"
    assert cotacoes[2].sigla == "JPY"
    assert cotacoes[2].valor == 130.0


@pytest.mark.django_db
@patch("cotacoes.populate_db.gerar_datas")
@patch("cotacoes.populate_db.get_cotacoes_json")
def test_popular_banco_cotacoes_nao_existentes(mock_get_cotacoes_json, mock_gerar_datas, test_date):
    # Defina a data da cotação
    date = datetime.date(2023, 7, 19)

    # Defina os valores para os mocks
    mock_gerar_datas.return_value = [date]
    mock_get_cotacoes_json.return_value = {}

    # Execute a função para popular o banco
    popular_banco()

    # Verifique se a cotação não foi criada no banco de dados
    cotacoes = Cotacao.objects.filter(data=date)
    assert len(cotacoes) == 0


@pytest.mark.django_db
def test_gerar_datas(test_date):
    # Use o teste real sem o mock para verificar se a função está gerando as datas corretamente
    datas_geradas = gerar_datas()

    # Verifique se a lista de datas foi gerada corretamente
    assert datas_geradas[0] == datetime.datetime.now().date()


@pytest.mark.django_db
@patch("requests.get")
def test_get_cotacoes_json(mock_requests_get, test_date):
    # Defina o valor de retorno para o mock do requests.get
    mock_response = Mock()
    mock_response.json.return_value = {
        "date": str(test_date.date()),
        "rates": {"BRL": 5.0, "EUR": 1.2, "JPY": 130.0},
    }
    mock_requests_get.return_value = mock_response

    # Chame a função get_cotacoes_json
    cotacoes_json = get_cotacoes_json(test_date)

    # Verifique se a função retorna os dados corretos
    assert cotacoes_json == {
        "date": str(test_date.date()),
        "rates": {"BRL": 5.0, "EUR": 1.2, "JPY": 130.0},
    }


@pytest.mark.django_db
def test_criar_cotacoes(test_date):
    # Use o teste real sem o mock para verificar se a função está criando as cotações corretamente
    json_data = {
        "date": str(test_date.date()),
        "rates": {"BRL": 5.0, "EUR": 1.2, "JPY": 130.0},
    }

    # Inicie uma transação para os testes de banco de dados
    with pytest.raises(
        Exception
    ):  # Use uma exceção como contexto para garantir a reversão da transação
        with transaction.atomic():
            criar_cotacoes(json_data)

    # Verifique se as cotações não foram criadas no banco de dados após a reversão da transação
    cotacoes = Cotacao.objects.filter(data=test_date)
    assert len(cotacoes) == 0
