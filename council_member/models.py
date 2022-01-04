from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
from associate.utils import claveAleatoria
from core import settings


class CouncilMember(models.Model):
    firstname = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nombre')
    lastname = models.CharField(max_length=200, null=True, blank=True, verbose_name='Apellidos')
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='council_member_user_set', verbose_name='Usuario'
    )
    is_active = models.BooleanField(default=True, verbose_name='Esta activo')
    circumscription_vote = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.SET_NULL, null=True,
        related_name='council_member_circumscription_set', verbose_name='Circunscripción'
    )
    voting_date = models.DateTimeField(null=True, verbose_name='Fecha de votación')
    email = models.EmailField(null=True, blank=True, verbose_name='Dirección de correo electrónico')
    password = models.CharField(max_length=50, null=True, blank=True, verbose_name='Clave')

    def get_clave(self):
        if not self.password or not len(self.password) == settings.LONGITUD_CLAVE:
            self.clave = claveAleatoria()
            self.save()
        return self.clave

    class Meta:
        verbose_name = 'Miembro del consejo'
        verbose_name_plural = 'Miembros del consejo'
