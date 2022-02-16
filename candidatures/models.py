from django.core.validators import MaxLengthValidator
from django.db import models


# Create your models here.
class Candidature(models.Model):
    filing_date = models.DateTimeField(auto_now=True, verbose_name='Fecha presentación candidatura')
    announcement = models.IntegerField(verbose_name='Convocatoria (0=No confirmada)', default=0)
    firstname = models.CharField(max_length=100, verbose_name='Nombre')
    lastname = models.CharField(max_length=100, verbose_name='Apellidos')
    presents_it = models.ForeignKey(
        'council_member.CouncilMember', null=True, related_name='candidature_council_member_set',
        on_delete=models.CASCADE, verbose_name='¿Quien lo presenta?', blank=True
    )
    partner_number = models.CharField(max_length=20, verbose_name='Nº de socio/a', null=True)
    locality = models.CharField(max_length=200, verbose_name='Localidad')
    circumscription = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.CASCADE, verbose_name='Circunscripción',
        related_name='candidature_circumscription_set'
    )
    seniority_date = models.DateField(null=True, verbose_name='Fecha antigüedad', blank=True)
    description = models.TextField(
        max_length=150, blank=True, validators=[MaxLengthValidator(150)],
        verbose_name='Breve descripción -máximo 150 caracteres'
    )
    curriculum_vitae = models.TextField(
        max_length=1000, validators=[MaxLengthValidator(1000)],
        verbose_name='Currículum profesional -máximo 1.000 caracteres'
    )
    bonding = models.TextField(
        max_length=1000, validators=[MaxLengthValidator(1000)],
        verbose_name='Vinculación con Greenpeace -máximo 1.000 caracteres'
    )
    motivation = models.TextField(
        max_length=1000, validators=[MaxLengthValidator(1000)],
        verbose_name='Motivación para presentar la candidatura -máximo 1.000 caracteres'
    )
    campaign = models.TextField(
        max_length=1000, validators=[MaxLengthValidator(1000)],
        verbose_name='¿Qué cambios te gustaría ver en Greenpeace en los próximos tres años? -máximo 1.000 caracteres'
    )
    dni = models.FileField(upload_to="%Y/%m/%d", verbose_name='Copia del DNI/ Pasaporte/ Tarjeta de residente')
    dni_number = models.CharField(
        max_length=100, verbose_name='Número y letra del DNI/ Pasaporte/ Tarjeta de residente'
    )
    presents_it_dni = models.FileField(
        upload_to="%Y/%m/%d", null=True, blank=True,
        verbose_name='Miembro del Consejo que presenta al candidato/a: Copia del DNI/ Pasaporte/ Tarjeta de residente',
    )
    photo = models.ImageField(
        upload_to="core/static/%Y/%m/%d", verbose_name=u'Foto -máximo 200kB-', null=True, blank=True
    )
    email = models.EmailField(
        verbose_name='Correo electrónico para facilitar a la comisión electoral la resolución de errores'
    )
    active_participation = models.BooleanField(
        verbose_name='Compromiso de participación activa: Al presentar esta candidatura adquiero el compromiso, en '
                     'caso de resultar elegido/a, de participar activamente en las tareas que el Consejo tiene '
                     'señaladas o se señalen.'
    )
    up_to_date = models.BooleanField(default=True, verbose_name='Al corriente de pago')
    veracity = models.BooleanField(verbose_name='Doy fe de la veracidad de los datos')
    is_adult = models.BooleanField(verbose_name='¿Es mayor de edad?', default=False)
    antiquity_3_years = models.BooleanField(verbose_name='Antigüedad > 3 años', default=False)
    validated_by_system = models.BooleanField(verbose_name='Comprobada por el sistema', default=False)
    validated_circumscription = models.BooleanField(verbose_name='Circunscripción correcta', default=False)
    validated = models.BooleanField(verbose_name='Validada', default=False)
    comments = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)], verbose_name='Comentarios'
    )
    allegations = models.TextField(
        max_length=1000, blank=True, validators=[MaxLengthValidator(1000)], verbose_name='Alegaciones'
    )
    is_allegate = models.BooleanField(default=False, verbose_name='Tiene alegaciones')
    on_the_council = models.BooleanField(default=False, verbose_name='Actualmente en el Consejo')
    participation = models.TextField(
        max_length=300, blank=True, validators=[MaxLengthValidator(300)], verbose_name='Participación'
    )

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

    def cuentaVotos(self):
        return self.vote_candidate_set.count()

    class Meta:
        verbose_name = 'Candidatura'
        verbose_name_plural = 'Candidaturas'
