from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from admin.salesforce import check_dni_salesforce
from candidatures.forms import AllegationForm
from candidatures.models import Candidature
from candidatures.utils import presentation, confirm, allegation, view_candidatures, send_allegation_mail


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


def view_candidate_details(request, num):
    candidate = Candidature.objects.get(pk=num)
    context = {'candidate': candidate}
    return render(request, 'candidate-details.html', context=context)


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
            check = check_dni_salesforce(request.POST.get('dni_number'))
            if not check:
                message = 'El DNI introducido no corresponde a ningún socio en activo, se puede actualizar en ' \
                          'la WEB de Greenpeace en Mi Perfil https://miperfil.greenpeace.es/'
                messages.add_message(request, messages.WARNING, message)
                return render(request, 'presentation.html', {'form': form})
            msg = f'Presentada por {check["Name"]} - {form.cleaned_data["dni_number"]} - {check["Email"]}: '
            candidate.allegations += '\r\n\r\n' + msg + form.cleaned_data['alegacion']
            candidate.is_allegate = True
            candidate.validated = False
            candidate.save()
            send_allegation_mail(candidate, msg)
            return HttpResponseRedirect('/alegacion_ok/')

    else:
        form = AllegationForm()

    context = {'candidate': candidate, 'form': form}
    return render(request, 'allegation_form.html', context=context)


def allegation_ok(request):
    return render(request, 'allegation_ok.html')
