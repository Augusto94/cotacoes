import pytest
from django.utils import timezone

from cotacoes.models import Cotacao


@pytest.fixture
def cotacao_data():
    return {
        "moeda": "Libra",
        "sigla": "GBP",
        "valor": 6.08,
        "data": timezone.now(),
    }


@pytest.mark.django_db
def test_criar_cotacao(cotacao_data):
    cotacao = Cotacao.objects.create(**cotacao_data)
    assert cotacao.moeda == cotacao_data["moeda"]
    assert cotacao.sigla == cotacao_data["sigla"]
    assert cotacao.valor == cotacao_data["valor"]
    assert cotacao.data == cotacao_data["data"]


@pytest.mark.django_db
def test_atualizar_cotacao(cotacao_data):
    cotacao = Cotacao.objects.create(**cotacao_data)
    nova_data = timezone.now()
    cotacao.moeda = "Libra Esterlina"
    cotacao.data = nova_data
    cotacao.save()

    cotacao_atualizada = Cotacao.objects.get(pk=cotacao.pk)
    assert cotacao_atualizada.moeda == "Libra Esterlina"
    assert cotacao_atualizada.data == nova_data


@pytest.mark.django_db
def test_deletar_cotacao(cotacao_data):
    cotacao = Cotacao.objects.create(**cotacao_data)
    cotacao_pk = cotacao.pk
    cotacao.delete()

    with pytest.raises(Cotacao.DoesNotExist):
        Cotacao.objects.get(pk=cotacao_pk)


@pytest.mark.django_db
def test_buscar_cotacao_por_sigla(cotacao_data):
    Cotacao.objects.create(**cotacao_data)
    cotacao_encontrada = Cotacao.objects.get(sigla=cotacao_data["sigla"])

    assert cotacao_encontrada.moeda == cotacao_data["moeda"]
    assert cotacao_encontrada.sigla == cotacao_data["sigla"]
    assert cotacao_encontrada.valor == cotacao_data["valor"]
    assert cotacao_encontrada.data == cotacao_data["data"]


@pytest.mark.django_db
def test_listar_cotacoes(cotacao_data):
    cotacao1 = Cotacao.objects.create(**cotacao_data)
    cotacao2_data = {
        "moeda": "Dólar neozelandês",
        "sigla": "NZD",
        "valor": 2.94,
        "data": timezone.now(),
    }
    cotacao2 = Cotacao.objects.create(**cotacao2_data)

    cotacoes = Cotacao.objects.all()

    assert cotacoes.count() == 2
    assert cotacao1 in cotacoes
    assert cotacao2 in cotacoes
