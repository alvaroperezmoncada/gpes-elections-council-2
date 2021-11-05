from django.core.validators import MaxLengthValidator
from django.db import models


# Create your models here.
class Candidature(models.Model):
    filing_date = models.DateTimeField(auto_now=True, verbose_name=u'Fecha presentación candidatura')
    firstname = models.CharField(max_length=100, verbose_name='Nombre')
    lastname = models.CharField(max_length=100, verbose_name='Apellidos')
    circumscription = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.CASCADE, verbose_name='Circunscripción',
        related_name='candidature_circumscription_set'
    )
    seniority_date = models.DateTimeField(null=True, verbose_name='Fecha antigüedad')
    description = models.TextField(
        max_length=150, blank=True, validators=[MaxLengthValidator(150)],
        verbose_name='Breve descripción -máximo 150 caracteres'
    )
    curriculum_vitae = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)],
        verbose_name='Currículum profesional -máximo 1.000 caracteres'
    )
    bonding = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)],
        verbose_name='Vinculación con Greenpeace -máximo 1.000 caracteres'
    )
    motivation = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)],
        verbose_name='Motivación para presentar la candidatura -máximo 1.000 caracteres'
    )
    campaign = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)], verbose_name='Campaña'
    )
    comments = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)], verbose_name='Comentarios'
    )
    allegations = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)], verbose_name='Alegaciones'
    )
    dni_number = models.CharField(max_length=200)
    email = models.EmailField()
    active_participation = models.BooleanField()
    up_to_date = models.BooleanField(default=True)
    veracity = models.BooleanField()
    antiquity_3_years = models.BooleanField()
    on_the_council = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Candidatura'
        verbose_name_plural = 'Candidaturas'
