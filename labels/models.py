from django.db import models

class Product(models.Model):
    codigo = models.CharField(max_length=100, unique=True, verbose_name="Código")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    codigo_de_barras = models.CharField(max_length=100, blank=True, null=True, verbose_name="Código de Barras")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

