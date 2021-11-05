from django.db import models


# Create your models here.
class Circumscription(models.Model):
    ds = models.CharField(max_length=100)
    alize = models.CharField(max_length=100)
    cod_ine = models.CharField(max_length=2, verbose_name='Cod. ine')
    places = models.IntegerField(verbose_name='Puestos')
    order = models.IntegerField(verbose_name='Orden')

    def __str__(self):
        return self.ds

    class Meta:
        verbose_name = 'Circunscripcion'
        verbose_name_plural = 'Circunscipciones'
        ordering = ['order', 'ds']
