from django.db import models


# Create your models here.
class Circumscription(models.Model):
    ds = models.CharField(max_length=100)
    alize = models.CharField(max_length=100)
    cod_ine = models.CharField(max_length=2, verbose_name='Cod. ine')
    places = models.IntegerField(verbose_name='Puestos')
    order = models.IntegerField(verbose_name='Orden')
    associate_number = models.IntegerField(verbose_name='Número de socios')

    def __str__(self):
        return self.ds

    def cuentaPapeletas(self):
        return self.ballot_circumscription_set.count()

    def cuentaPapeletasVerificadas(self):
        if self.id == 19:
            return self.council_member_circumscription_set.count()
        return self.associate_circumscription_vote_set.count()

    def cuentaVotoBlanco(self):
        return self.ballot_circumscription_set.filter(blank_vote=True).count()

    def cuentaVotoNulo(self):
        return self.ballot_circumscription_set.filter(null_vote=True).count()

    def cuentaVotantes(self):
        return self.associate_number

    def indiceParticipacion(self):
        if self.cuentaVotantes():
            ret = round(100.0 * self.cuentaPapeletas() / self.cuentaVotantes(), 2)
            return ('%0.2f' % (ret,)).replace('.', ',')
        else:
            return 'n/a'

    def candidatos_ordenados(self):
        return self.candidature_circumscription_set.filter(validated=True, announcement__gt=0). \
            order_by('seniority_date')

    def candidatos_ordenados_por_voto(self):
        ret = list(self.candidature_circumscription_set.filter(
            validated=True, announcement__gt=0, seniority_date__isnull=False
        ))
        ret.sort(key=lambda c: (-c.cuentaVotos(), c.seniority_date))
        for n, c in enumerate(ret):
            c.electo = (n < (self.places or 15) and c.cuentaVotos())
        for c in ret:
            print(c.electo, c.firstname, c.cuentaVotos())
        return ret

    def candidatos_ordenados_60(self):
        return self.candidatos_ordenados().filter(announcement=60)

    def cuenta_candidatos_60(self):
        return self.candidatos_ordenados_60().count()

    def candidatos_ordenados_15(self):
        return self.candidatos_ordenados().filter(announcement=15)

    def cuenta_candidatos_15(self):
        return self.candidatos_ordenados_15().count()

    class Meta:
        verbose_name = 'Circunscripcion'
        verbose_name_plural = 'Circunscipciones'
        ordering = ['ds', 'order']
