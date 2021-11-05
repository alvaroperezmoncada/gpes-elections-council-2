from django.db import models


# Create your models here.
class Deadline(models.Model):
    ds = models.CharField(max_length=100)
    module = models.CharField(max_length=100, verbose_name='Módulo')
    start_dt = models.DateTimeField(verbose_name='Fecha de inicio')
    end_dt = models.DateTimeField(verbose_name='Fecha de fin')

    def __str__(self):
        return self.ds

    class Meta:
        verbose_name = 'Plazo'
        verbose_name_plural = 'Plazos'
        ordering = ('end_dt',)
