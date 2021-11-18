from django import forms
from django.forms import ModelForm, Form

from candidatures.models import Candidature


class NewCandidatureForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'firstname', 'lastname', 'locality', 'circumscription', 'curriculum_vitae', 'bonding', 'motivation',
            'campaign', 'dni', 'dni_number', 'photo', 'email', 'active_participation', 'veracity'
        ]


class NewCandidatureConfirmForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'firstname', 'lastname', 'locality', 'circumscription', 'curriculum_vitae', 'bonding', 'motivation',
            'campaign', 'email'
        ]


class NewCandidature15Form(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'presents_it', 'presents_it_dni', 'firstname', 'lastname', 'locality', 'curriculum_vitae', 'bonding', 'dni',
            'dni_number', 'photo', 'email', 'active_participation', 'veracity'
        ]


class AllegationForm(Form):
    alegacion = forms.CharField(max_length=200, widget=forms.Textarea)
