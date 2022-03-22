from django import forms
from django.forms import ModelForm

from candidatures.models import Candidature


class AdminCandidateForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'validated', 'validated_by_system', 'antiquity_3_years', 'up_to_date', 'is_adult', 'on_the_council',
            'validated_circumscription', 'partner_number', 'firstname', 'lastname', 'locality', 'circumscription',
            'dni_number', 'email', 'photo', 'dni', 'curriculum_vitae', 'bonding', 'motivation', 'campaign',
            'participation',

        ]
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'partner_number': forms.TextInput(attrs={'class': 'form-control'}),
            'circumscription': forms.Select(attrs={'class': 'form-control'}),
            'curriculum_vitae': forms.Textarea(attrs={'class': 'form-control form-control2'}),
            'bonding': forms.Textarea(attrs={'class': 'form-control form-control2'}),
            'motivation': forms.Textarea(attrs={'class': 'form-control form-control2'}),
            'campaign': forms.Textarea(attrs={'class': 'form-control form-control2'}),
            'participation': forms.Textarea(attrs={'class': 'form-control form-control2'}),
            'dni_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
