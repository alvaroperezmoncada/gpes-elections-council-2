from django.forms import ModelForm

from candidatures.models import Candidature


class AdminCandidateForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'validated', 'validated_by_system', 'antiquity_3_years', 'up_to_date', 'is_adult', 'partner_number',
            'validated_circumscription', 'firstname', 'lastname', 'locality', 'circumscription',
            'curriculum_vitae', 'bonding', 'motivation', 'campaign', 'dni', 'dni_number', 'photo', 'email',
            'on_the_council', 'participation',
        ]
