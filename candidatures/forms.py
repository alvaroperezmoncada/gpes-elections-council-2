from django.forms import ModelForm

from candidatures.models import Candidature


class NewCandidature(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'firstname', 'lastname', 'circumscription', 'curriculum_vitae', 'bonding', 'motivation', 'campaign',
            'dni_number', 'email', 'active_participation', 'veracity'
        ]
