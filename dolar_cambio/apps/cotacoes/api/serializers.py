from rest_framework import serializers

from cotacoes.models import Cotacao


class CotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = [
            "id",
            "moeda",
            "sigla",
            "valor",
            "data",
        ]
