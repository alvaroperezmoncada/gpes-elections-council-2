from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class CouncilMember(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='council_member_user_set', verbose_name='Usuario'
    )
    is_active = models.BooleanField(default=True, verbose_name='Esta activo')
    circumscription = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.SET_NULL, null=True,
        related_name='council_member_circumscription_set', verbose_name='Circunscripción'
    )
    voting_date = models.DateTimeField(null=True, verbose_name='Fecha de votación')

    class Meta:
        verbose_name = 'Miembro del consejo'
        verbose_name_plural = 'Miembros del consejo'
