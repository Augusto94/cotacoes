from django.contrib import admin

from cotacoes.models import Cotacao


@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):

    search_fields = ["moeda", "sigla", "data"]
    list_display = ("moeda", "sigla", "valor", "data")
    ordering = ("-data",)
