from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Ballot(models.Model):
    circumscription = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.SET_NULL, null=True,
        related_name='ballot_circumscription_set', verbose_name='Circunscripción'
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True,
        related_name='ballot_user_set', verbose_name='Usuario'
    )
    voting_date = models.DateTimeField(null=True, verbose_name='Fecha de votación')
    blank_vote = models.BooleanField(verbose_name='Voto en blanco')
    null_vote = models.BooleanField(verbose_name='Voto nulo')

    def __str__(self):
        return f'{self.circumscription} {self.user} {self.voting_date}'

    def listaCandidatos(self):
        ret = list(self.vote_ballot_set.all())
        ret.sort(key=lambda x: x.candidato.fecha_alta)
        return ret

    class Meta:
        verbose_name = 'Papeleta'
        verbose_name_plural = 'Papeletas'


class Vote(models.Model):
    candidate = models.ForeignKey(
        'circumscription.Circumscription', on_delete=models.CASCADE, related_name='vote_candidate_set'
    )
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name='vote_ballot_set')

    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'

    def __str__(self):
        return u'%s %s' % (self.candidate, self.ballot)
