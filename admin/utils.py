from itertools import groupby

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date

from admin.forms import AdminCandidateForm
from admin.salesforce import get_contact
from candidatures.models import Candidature
from core import settings
from deadlines.models import Deadline
from provinces.models import Province


def get_active_modules(request):
    dt_now = timezone.now()
    queryset = Deadline.objects.all()
    if not request.user.is_superuser:
        queryset = queryset.filter(start_dt__lte=dt_now, end_dt__gte=dt_now)
    return queryset.values()


def commision(request, _type):
    full = request.GET.get('full', False)
    candidates = Candidature.objects.filter(announcement=_type)
    valid_candidates = candidates.filter(validated=True).order_by('circumscription', 'seniority_date')
    not_valid_candidates = candidates.filter(validated=False).order_by('lastname', 'firstname')

    ccaa = [(k, list(v)) for (k, v) in groupby(valid_candidates, lambda x: x.circumscription)]
    context = {
        'ccaa': ccaa,
        'not_valid_candidates': not_valid_candidates,
        'full': full
    }

    return render(request, 'admin_candidates.html', context=context)


def edit_candidate(request, _type, _id):
    candidate = Candidature.objects.get(pk=_id)
    assert candidate.announcement == _type

    if request.method == 'POST':
        form = AdminCandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/comision_{_type}/')
        info = {'info': 'Se han detectado errores'}

    else:
        if candidate.validated_by_system:
            info = {'info': 'Ya validado'}
        else:
            info = get_contact(candidate.email, candidate.dni_number)
            if info:
                if info['Income_ultimos_12_meses_CONSEJO__c'] >= settings.MIN_INCOME:
                    candidate.up_to_date = True
                    candidate.save()
                if info['Birthdate']:
                    candidate.fecha_nacimiento = parse_date(info['Birthdate'])
                    if candidate.fecha_nacimiento <= settings.FECHA_MAXIMA_NACIMIENTO:
                        candidate.is_adult = True
                    candidate.save()
                if info['Fecha_de_antiguedad__c']:
                    candidate.seniority_date = parse_date(info['Fecha_de_antiguedad__c'])
                    candidate.antiquity_3_years = candidate.seniority_date <= settings.FECHA_MAXIMA_ANTIGUEDAD
                    candidate.save()
                if _type == 15:
                    candidate.validated_circumscription = True
                elif info['MailingPostalCode']:
                    prefijo = info['MailingPostalCode'][:2]
                    circunscripcion_por_cp = Province.objects.get(prefix_cp=prefijo).circumscription
                    candidate.validated_circumscription = candidate.circumscription == circunscripcion_por_cp
                    candidate.save()
                candidate.validated_by_system = (
                        candidate.up_to_date is True and candidate.validated_by_system is True
                        and candidate.is_adult is True and candidate.antiquity_3_years is True
                )
                candidate.save()
            else:
                info = {'info': 'Sin resultados'}
        form = AdminCandidateForm(instance=candidate)

    context = {'candidato': candidate, 'form': form, 'info': info}
    return render(request, 'edit_candidates.html', context)
