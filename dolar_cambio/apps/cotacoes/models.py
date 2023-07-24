from django.db import models


class Cotacao(models.Model):
    moeda = models.CharField(max_length=30)
    sigla = models.CharField(max_length=3)
    valor = models.FloatField(null=True, blank=True)
    data = models.DateTimeField()

    class Meta:
        verbose_name = "Cotação"
        verbose_name_plural = "Cotações"
