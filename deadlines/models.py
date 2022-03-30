from django.db import models


# Create your models here.
class Deadline(models.Model):
    ds = models.CharField(max_length=100)
    module = models.CharField(max_length=100, verbose_name='Módulo')
    start_dt = models.DateTimeField(verbose_name='Fecha de inicio')
    end_dt = models.DateTimeField(verbose_name='Fecha de fin')
    announcement = models.IntegerField(verbose_name='Convocatoria (0=No confirmada)', default=60)

    def __str__(self):
        return self.ds

    def star_dt_humanize(self):
        return self.start_dt.strftime('%d-%m-%Y %H:%M:%S')

    def end_dt_humanize(self):
        return self.end_dt.strftime('%d-%m-%Y %H:%M:%S')

    class Meta:
        verbose_name = 'Plazo'
        verbose_name_plural = 'Plazos'
        ordering = ('ds',)
