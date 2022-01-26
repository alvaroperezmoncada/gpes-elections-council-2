from django.http import HttpResponseRedirect
from django.shortcuts import render

from candidatures.forms import AllegationForm
from candidatures.models import Candidature
from candidatures.utils import presentation, confirm, allegation, view_candidatures


# Funciones que controlan las candidaturas de los 60 candidatos.
def presentation60_view(request):
    return presentation(request, 60)


def confirm60_view(request):
    return confirm(request, 60)


def ok60(request):
    return render(request, 'ok_60.html')


def allegation60(request):
    return allegation(request, 60)


def view_candidatures60(request):
    return view_candidatures(request, 60)


# Funciones que controlan las 15 candidaturas que presentan los miembros del consejo.
def presentation15_view(request):
    return presentation(request, 15)


def confirm15_view(request):
    return confirm(request, 15)


def ok15(request):
    return render(request, 'ok_15.html')


def allegation15(request):
    return allegation(request, 15)


def view_candidatures15(request):
    return view_candidatures(request, 15)


def allegate(request, num):
    candidate = Candidature.objects.get(pk=num)
    if request.method == 'POST':
        form = AllegationForm(request.POST)
        if form.is_valid():
            msg = f'Presentada por DNI: {form.cleaned_data["dni_number"]}: '
            candidate.allegations += '\r\n\r\n' + msg + form.cleaned_data['alegacion']
            candidate.is_allegate = True
            candidate.validated = False
            candidate.save()
            return HttpResponseRedirect('/alegacion_ok/')

    else:
        form = AllegationForm()

    context = {'candidate': candidate, 'form': form}
    return render(request, 'allegation_form.html', context=context)


def allegation_ok(request):
    return render(request, 'allegation_ok.html')
