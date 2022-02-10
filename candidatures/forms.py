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

    def clean_active_participation(self):
        data = self.cleaned_data['active_participation']
        if not data:
            raise forms.ValidationError('Para enviar la candidatura, debes aceptar el compromiso de participación')
        return data

    def clean_photo(self):
        data = self.cleaned_data['photo']
        max_size = 256 * 1024
        if data and len(data) > max_size:
            raise forms.ValidationError(f'El tamaño esta resgtringido a {max_size / 1024} KB')
        return data

    def clean_veracity(self):
        data = self.cleaned_data['veracity']
        if not data:
            forms.ValidationError('Para enviar la candidatura, debes dar fé de la veracidad de los datos')
        return data

    def clean_curriculum_vitae(self):
        data = self.cleaned_data['curriculum_vitae']
        return data.replace('\r\n', '\r')

    def clean_bonding(self):
        data = self.cleaned_data['bonding']
        return data.replace('\r\n', '\r')


class NewCandidatureConfirmForm(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'firstname', 'lastname', 'locality', 'circumscription', 'curriculum_vitae', 'bonding', 'motivation',
            'campaign', 'dni_number', 'email'
        ]


class NewCandidature15Form(ModelForm):
    class Meta:
        model = Candidature
        fields = [
            'presents_it', 'presents_it_dni', 'firstname', 'lastname', 'locality', 'curriculum_vitae', 'bonding', 'dni',
            'dni_number', 'photo', 'email', 'active_participation', 'veracity'
        ]

    def clean_presents_it(self):
        data = self.cleaned_data['presents_it']
        if not data:
            raise forms.ValidationError('Se debe indicar qué consejor/a presenta al nuevo candidato/a')
        return data

    def clean_active_participation(self):
        data = self.cleaned_data['active_participation']
        if not data:
            raise forms.ValidationError('Para enviar la candidatura, debes aceptar el compromiso de participación')
        return data

    def clean_photo(self):
        data = self.cleaned_data['photo']
        max_size = 256 * 1024
        if data and len(data) > max_size:
            raise forms.ValidationError(f'El tamaño esta resgtringido a {max_size / 1024} KB')
        return data

    def clean_veracity(self):
        data = self.cleaned_data['veracity']
        if not data:
            forms.ValidationError('Para enviar la candidatura, debes dar fé de la veracidad de los datos')
        return data

    def clean_curriculum_vitae(self):
        data = self.cleaned_data['curriculum_vitae']
        return data.replace('\r\n', '\r')

    def clean_bonding(self):
        data = self.cleaned_data['bonding']
        return data.replace('\r\n', '\r')


class AllegationForm(Form):
    dni_number = forms.CharField(max_length=200, label='DNI de quien alega')
    alegacion = forms.CharField(max_length=200, widget=forms.Textarea, label='Alegación')
