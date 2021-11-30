from itertools import groupby

from django.forms import Select
from django.http import HttpResponseRedirect
from django.shortcuts import render

from candidatures.forms import NewCandidatureForm, NewCandidatureConfirmForm, NewCandidature15Form
from candidatures.models import Candidature


def presentation(request, _type):
    form = NewCandidatureForm if _type == 60 else NewCandidature15Form
    if request.method == 'POST':
        form = form(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            request.session['candidate_id'] = candidate.id
            return HttpResponseRedirect(f'confirmar_{_type}')
    return render(request, 'presentation.html', {'form': form})


def confirm(request, _type):
    candidate = Candidature.objects.get(pk=request.session['candidate_id'])
    if request.method == 'POST':  # If the form has been submitted...
        candidate.announcement = _type
        candidate.partner_number = 'n/a'
        candidate.save()
        # envia_confirmacion(candidate)
        return HttpResponseRedirect(f'/ok_{_type}')
    else:
        form = NewCandidatureConfirmForm(instance=candidate)
        c = dict(form=form, candidate=candidate)
        for k in form.fields:
            w = form.fields[k].widget
            if isinstance(w, Select):
                w.attrs['disabled'] = True
            else:
                w.attrs['readonly'] = True

        return render(request, 'presentation_preview.html', c)


def allegation(request, _type):
    candidate = Candidature.objects.filter(announcement=_type)
    valid_candidate = candidate.filter(validated=True).order_by('circumscription', 'seniority_date')
    not_valid_candidate = candidate.exclude(validated=True).order_by('lastname', 'firstname')

    ccaa = [(k, list(v)) for (k, v) in groupby(valid_candidate, lambda x: x.circumscription)]
    context = {'ccaa': ccaa, 'not_valid_candidate': not_valid_candidate}
    return render(request, 'allegations.html', context=context)


def view_candidatures(request, _type):
    candidates = Candidature.objects.filter(announcement=_type)
    valid_candidates = candidates.filter(validated=True).order_by('circumscription', 'seniority_date')
    ccaa = [(k, list(v)) for (k, v) in groupby(valid_candidates, lambda x: x.circumscription)]
    context = {'ccaa': ccaa}
    return render(request, 'view_candidatures.html', context=context)