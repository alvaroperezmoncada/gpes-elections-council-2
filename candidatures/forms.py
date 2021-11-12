from django.forms import ModelForm

from candidatures.models import Candidature


class NewCandidatureForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'firstname', 'lastname', 'locality', 'circumscription', 'curriculum_vitae', 'bonding', 'motivation',
            'campaign', 'dni', 'photo', 'email', 'active_participation', 'veracity'
        ]


class NewCandidatureConfirmForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'firstname', 'lastname', 'locality', 'circumscription', 'curriculum_vitae', 'bonding', 'motivation',
            'campaign', 'email'
        ]
