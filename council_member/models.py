from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
from django.utils import timezone

from associate.utils import claveAleatoria
from core import settings


class CouncilMember(models.Model):
    firstname = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nombre')
    lastname = models.CharField(max_length=200, null=True, blank=True, verbose_name='Apellidos')
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='council_member_user_set', verbose_name='Usuario',
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Esta activo')
    circumscription_vote = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='council_member_circumscription_set', verbose_name='Circunscripción'
    )
    voting_date = models.DateTimeField(null=True, verbose_name='Fecha de votación', blank=True)
    email = models.EmailField(null=True, blank=True, verbose_name='Dirección de correo electrónico')
    password = models.CharField(max_length=50, null=True, blank=True, verbose_name='Clave')

    def __str__(self):
        return f'{self.lastname or ""} {self.firstname or ""}'

    def get_clave(self):
        if not self.password or not len(self.password) == settings.LONGITUD_CLAVE:
            self.clave = claveAleatoria()
            self.save()
        return self.clave

    def fecha_voto_legible(self):
        return self.voting_date.strftime("%H:%M %d-%m-%Y")

    def can_vote(self):
        if self.voting_date:
            return False, 'Ya se ha registrado un voto'
        return True, ''

    def registraVoto(self, usuario):
        assert self.can_vote()[0]
        self.circumscription_vote_id = 19
        self.usuario = usuario
        self.fecha_voto = timezone.now()

    def desregistraVoto(self):
        assert not self.can_vote()[0]
        self.voting_date = None
        self.circumscription_vote_id = None
        self.user = None

    class Meta:
        verbose_name = 'Miembro del consejo'
        verbose_name_plural = 'Miembros del consejo'
