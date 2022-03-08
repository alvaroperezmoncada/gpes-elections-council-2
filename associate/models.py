from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from associate.utils import claveAleatoria
from core import settings


class Associate(models.Model):
    firstname = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nombre')
    lastname = models.CharField(max_length=200, null=True, blank=True, verbose_name='Apellidos')
    dni_number = models.CharField(max_length=200, blank=True, verbose_name='Documento de indentidad')
    associate_number = models.CharField(max_length=200, verbose_name='Número de socio/a')
    circumscription = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.SET_NULL, null=True,
        related_name='associate_circumscription_set', verbose_name='Circunscripción'
    )
    associate_dt = models.DateField(null=True, blank=True, verbose_name='Fecha antigüedad')
    voting_date = models.DateTimeField(null=True, verbose_name='Fecha de votación', blank=True)
    birthday = models.DateTimeField(null=True, verbose_name='Fecha de nacimiento', blank=True)
    circumscription_vote = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='associate_circumscription_vote_set', verbose_name='Circunscripción voto'
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='associate_user_set', verbose_name='Usuario',
        null=True, blank=True
    )
    email = models.EmailField(null=True, blank=True, verbose_name='Dirección de correo electrónico')
    password = models.CharField(max_length=50, null=True, blank=True, verbose_name='Clave')

    def __str__(self):
        return f'{self.lastname or ""} {self.firstname or ""}'

    def can_vote(self):
        if self.voting_date:
            return False, 'Ya se ha registrado un voto'
        return True, ''

    def get_clave(self):
        if not self.password or not len(self.password) == settings.LONGITUD_CLAVE:
            self.password = claveAleatoria()
            self.save()
        return self.password

    class Meta:
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['firstname', 'lastname']
