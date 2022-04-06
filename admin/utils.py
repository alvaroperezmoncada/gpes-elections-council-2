import datetime
from itertools import groupby

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date

from admin.forms import AdminCandidateForm
from admin.salesforce import get_contact, MultipleContactsError, searchContacts
from associate.models import Associate
from ballot.models import Ballot, Vote
from candidatures.models import Candidature
from circumscription.models import Circumscription
from core import settings
from council_member.models import CouncilMember
from deadlines.models import Deadline
from provinces.models import Province


def get_active_modules(request):
    dt_now = timezone.now()
    queryset = Deadline.objects.all()
    if not request.user.is_superuser:
        queryset = queryset.filter(start_dt__lte=dt_now, end_dt__gte=dt_now)
    return queryset.values().order_by('ds')


def is_active_module(request, module):
    active_modules = get_active_modules(request)
    return active_modules.filter(module=module)


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def commision(request, _type):
    if not is_active_module(request, 'comision_%s' % _type) and not request.user.is_superuser:
        return HttpResponseRedirect('/')
    full = request.GET.get('full', False)
    candidates = Candidature.objects.filter(announcement=_type)
    valid_candidates = candidates.filter(validated=True).order_by('circumscription', 'seniority_date')
    not_valid_candidates = candidates.filter(validated=False).order_by('lastname', 'firstname')

    ccaa = [(k, list(v)) for (k, v) in groupby(valid_candidates, lambda x: x.circumscription)]
    context = {
        'ccaa': ccaa,
        'not_valid_candidates': not_valid_candidates,
        'full': full,
        'announcement': _type
    }

    return render(request, 'admin_candidates.html', context=context)


def edit_candidate(request, _type, _id):
    if not is_active_module(request, 'comision_%s' % _type) and not request.user.is_superuser:
        return HttpResponseRedirect('/')
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

                if info['AlizeConstituentID__c']:
                    candidate.partner_number = info['AlizeConstituentID__c']
                    candidate.save()

                candidate.validated_by_system = candidate.validated = (
                        candidate.is_adult is True and candidate.antiquity_3_years is True and candidate.up_to_date is True
                        and candidate.validated_circumscription is True

                )
                candidate.save()
            else:
                info = {'info': 'Sin resultados'}
        form = AdminCandidateForm(instance=candidate)

    context = {'candidato': candidate, 'form': form, 'info': info}
    return render(request, 'edit_candidates.html', context)


def vote(request, _type, voting_class):
    if request.method != 'POST':
        return render(request, 'vote.html', context={'tipo': _type})
    dni = request.POST.get('email')
    if dni:
        if _type == 60:
            info = get_contact(dni, dni)
            if info:
                email_db = info['Email']
                return render(request, 'vote_confirm.html', context={'tipo': _type, 'email': email_db, 'dni': dni})
            else:
                msg = u'''No hay ninguna persona en nuestra base de datos que cumpla esta condición.
                            Por favor, ponte en contacto con nuestra oficina, teléfono: 900 535 025,
                            correo electrónico: <a href="mailto:sociasysocios.es@greenpeace.org">sociasysocios.es@greenpeace.org</a>.
                            Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''
                level = messages.WARNING
                messages.add_message(request, level, msg)
        else:
            try:
                council = CouncilMember.objects.get(dni_number=dni)
            except CouncilMember.DoesNotExist:
                msg = u'''No hay ninguna persona en nuestra base de datos que cumpla esta condición.
                                            Por favor, ponte en contacto con nuestra oficina, teléfono: 900 535 025,
                                            correo electrónico: <a href="mailto:sociasysocios.es@greenpeace.org">sociasysocios.es@greenpeace.org</a>.
                                            Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''
                level = messages.WARNING
                messages.add_message(request, level, msg)
            else:
                return render(request, 'vote_confirm.html', context={'tipo': _type, 'email': council.email, 'dni': dni})
        return render(request, 'vote.html', context={'tipo': _type})
    password = request.POST['clave']
    try:
        member = voting_class.objects.get(password=password)
    except voting_class.DoesNotExist:
        message = 'Verifique la clave por favor'
        messages.add_message(request, messages.INFO, message)
        return render(request, 'vote.html', context={'tipo': _type})

    can_vote, msg = member.can_vote()
    if not can_vote:
        messages.add_message(request, messages.WARNING, u'No puede votar: %s' % msg)
        return HttpResponseRedirect('/')

    request.session['usu%s' % _type] = member.pk
    if _type == 15:
        return HttpResponseRedirect('/papeleta_%s/%s/' % (_type, 19))
    if _type == 60 and member.circumscription.pk != 19:
        return HttpResponseRedirect('/papeleta_%s/%s/' % (_type, member.circumscription.pk))
    else:
        return render(request, 'selector_usu.html', dict(tipo=_type, ccaa=Circumscription.objects.all()))


def send_pass(request, _type):
    if request.method != "POST":
        return HttpResponseRedirect('/')

    email = request.POST.get('email')
    if not email:
        return HttpResponseRedirect('/votacion_%s/' % _type)

    msg = ''
    if _type == 15:
        try:
            consejero = CouncilMember.objects.get(dni_number=email)
            email_text = u'Estimado/a %s\r\nÉsta es tu clave: %s' % (
                consejero.firstname, consejero.get_clave())
            send_mail(u"[Greenpeace España/Elecciones] Clave para votar ", email_text, 'no-reply@greenpeace.es',
                      [consejero.email],
                      fail_silently=False)
            msg = u'Por favor, verifica tu buzón de correo. En breve te llegará un mensaje con la clave para votar.'
            level = messages.SUCCESS
        except ObjectDoesNotExist:
            msg = u'''La votación está abierta solamente a los consejeros vigentes.
                Verifica que tu dirección de correo es la activa de la lista del
                Consejo'''
            level = messages.WARNING
        messages.add_message(request, level, msg)
        return HttpResponseRedirect('/votacion_%s/' % _type)

    try:
        info = get_contact(email, email)  # TODO cambiar a dni
        if info:
            num_socio = info[u'AlizeConstituentID__c']
            income = info['Income_ultimos_12_meses_CONSEJO__c']
            fecha_alta = parse_date(info['Activation_Date__c'])
            today = datetime.date.today()
            meses_active = min(12, diff_month(today, fecha_alta))
            if income / meses_active < settings.MIN_INCOME / 12:
                msg = u'''Parece que hay algún problema con el pago de tu cuota,
                por favor, ponte en contacto con nuestra oficina, teléfono: 900 535 025,
                correo electrónico:
                <a href="mailto:sociasysocios.es@greenpeace.org">sociasysocios.es@greenpeace.org</a>.
                Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''
            if info['Birthdate']:
                fecha_nacimiento = parse_date(info['Birthdate'])
                if fecha_nacimiento > settings.FECHA_MAXIMA_NACIMIENTO:
                    msg = u'''Para poder participar en estas elecciones necesitabas ser mayor de edad
                    en el momento de la convocatoria. Te esperamos en las próximas elecciones'''
            else:
                msg = u'''Para poder votar necesitas tener fecha de nacimiento en la base de 
                datos. Por favor, ponte en contacto con nuestra oficina, teléfono: 900 535 025, 
                correo electrónico: sociasysocios.es@greenpeace.org o actualízala en
                 Tu perfil greenpeace. Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''
            try:
                EmailValidator()(info['Email'])
            except ValidationError:
                msg = u'''Para poder votar electrónicamente, necesitamos que tengas una dirección de correo electrónico registrada en la base de datos de Greenpeace España para enviarte la clave. Por favor, ponte en contacto con nuestra oficina, teléfono: 900 535 025, correo electrónico: sociasysocios.es@greenpeace.org. Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''
            # if fecha_alta > settings.FECHA_CONVOCATORIA:
            #     msg = u'''Para poder participar en estas elecciones necesitabas pertenecer a Greenpeace España en el momento de su convocatoria. Te esperamos en las próximas elecciones.'''
            soc_local = Associate.objects.filter(associate_number=num_socio).exclude(voting_date=None).first()
            if soc_local:
                msg = u'''El sistema tiene registrado tu voto en {:%d-%m-%Y %H:%M}'''.format(soc_local.voting_date)
        else:
            msg = u'''No hay ninguna persona en nuestra base de datos que cumpla esta condición.
            Por favor, ponte en contacto con nuestra oficina, teléfono: 900 535 025,
            correo electrónico: <a href="mailto:sociasysocios.es@greenpeace.org">sociasysocios.es@greenpeace.org</a>.
            Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''
    except MultipleContactsError:
        info = None
        msg = u'''Hay más de una persona en nuestra base de datos que cumple esta
        condición.Por favor, ponte en contacto con nuestra oficina,
        teléfono: 900 535 025, correo electrónico: sociasysocios.es@greenpeace.org.
        Cuando esté resuelto, inténtalo de nuevo. Te esperamos.'''

    if msg == '':
        socio, created = Associate.objects.get_or_create(associate_number=num_socio)
        socio.email = info['Email']
        socio.firstname = info['Name']
        if info['MailingPostalCode']:
            prefijo = info['MailingPostalCode'][:2]
            try:
                circunscripcion_por_cp = Province.objects.get(prefix_cp=prefijo).circumscription
            except ObjectDoesNotExist:
                circunscripcion_por_cp = Circumscription.objects.get(id=19)
        else:
            circunscripcion_por_cp = Circumscription.objects.get(id=19)
        socio.circumscription = circunscripcion_por_cp
        socio.save()
        # socio.get_clave()
        email_text = u'Estimado/a %s\r\nÉsta es tu clave: %s' % (
            socio.firstname, socio.get_clave())
        send_mail(
            u"[Greenpeace España/Elecciones] Clave para votar ", email_text, 'no-reply@greenpeace.es', [socio.email],
            fail_silently=False
        )
        msg = f'Se enviará la clave al correo {info["Email"]}, si desea actualizar el correo acceder en la Web ' \
              f'de Greenpeace a Mi Perfil https://miperfil.greenpeace.es/'
        level = messages.SUCCESS
    else:
        level = messages.WARNING
    messages.add_message(request, level, msg)
    return HttpResponseRedirect('/votacion_%s/' % _type)


def ballot(request, ca, _type, voting_class):
    usu = request.session.get('usu%s' % _type)
    if not usu:
        return HttpResponseRedirect("/")
    socio = voting_class.objects.get(pk=usu)
    can_vote, msg = socio.can_vote()
    if not can_vote:
        mensaje = u'No puede votar en esta web; intente votar por correo postal: ' + msg
        messages.add_message(request, messages.SUCCESS, mensaje)
        return render(request, 'message_pub.html')
    circ = Circumscription.objects.get(pk=ca)
    plantilla = 'ballot_pub.html'
    if _type == 60:
        max_candidatos = circ.places
        assert socio.circumscription.pk == 19 or socio.circumscription == circ
    else:
        max_candidatos = settings.MAX_CANDIDATOS_15
    return render(request, 'ballot_pub.html', locals())


def register_vote(request, ca, _type, voting_class):
    if request.method == "GET":
        return HttpResponseRedirect('/')
    id_usu = request.session.get('usu%s' % _type)
    if not id_usu:
        return HttpResponseRedirect("/")
    circ = Circumscription.objects.get(pk=ca)
    usu = voting_class.objects.get(pk=id_usu)
    if _type == 60:
        assert usu.circumscription == 19 or circ.pk == usu.circumscription_id, 'Se está votando por una circ no autorizada'
    can_vote, msg = usu.can_vote()
    if not can_vote:
        messages.add_message(request, messages.WARNING, 'No puede votar: ' + msg)
        return HttpResponseRedirect('/')
    usu.voting_date = datetime.datetime.now()
    usu.save()
    papeleta = Ballot(circumscription=circ)
    aspas = [int(v) for k, v in request.POST.items() if k.startswith('cdto')]
    if _type == 60:
        max_candidatos = circ.places
    else:
        max_candidatos = settings.MAX_CANDIDATOS_15
    assert len(aspas) <= max_candidatos, u'No se puede votar a más candidatos que puestos'
    if request.POST.get('nulo'):
        assert not aspas, u'Aspas y nulo'
        papeleta.null_vote = True
        papeleta.blank_vote = False
    elif request.POST.get('blanco'):
        assert not aspas, u'Aspas y blanco'
        papeleta.blank_vote = True
        papeleta.null_vote = False
    else:
        assert aspas, u'Ni aspas ni blanco'
        papeleta.blank_vote = False
        papeleta.null_vote = False
    papeleta.save()
    for aspa in aspas:
        candidato = Candidature.objects.get(pk=aspa)
        # Sólo en caso de hostilidad
        assert candidato.circumscription.pk == circ.pk, u'Se está votando por candidatos de otra papeleta'
        voto = Vote(candidate=candidato, ballot=papeleta)
        voto.save()
    msg = u'<span style="font-size:300%;color:green;">Voto registrado</span>'
    messages.add_message(request, messages.SUCCESS, msg)
    email_text = 'Se ha registrado correctamente tu voto, gracias por participar.'
    send_mail(
        u"Registro exitoso, votaciones Greenpeace ", email_text, 'no-reply@greenpeace.es', [usu.email],
        fail_silently=False
    )
    return HttpResponseRedirect('/')


def results(request, _type):
    circumscription = Circumscription.objects.all()
    ccaa = circumscription.exclude(pk=19) if _type == 60 else circumscription.filter(pk=19)
    c = dict(ccaa=ccaa, tipo=_type)
    return render(request, 'results.html', c)


def selector(request, _type):
    if _type == 15:
        ccaa = Circumscription.objects.filter(id=19)
    else:
        ccaa = Circumscription.objects.exclude(id=19)

    total_papeletas = 0
    total_socios = 0
    indice_total = 'n/a'

    for circ in ccaa:
        votantes = circ.cuentaVotantes()
        papeletas = circ.cuentaPapeletas()
        total_socios += votantes
        total_papeletas += papeletas

    if total_socios > 0:
        ret = round(100.0 * total_papeletas / total_socios, 2)
        indice_total = ('%0.2f' % (ret,)).replace('.', ',')

    return render(
        request, 'selector.html', dict(
            ccaa=ccaa, tipo=_type, total_papeletas=total_papeletas, total_socios=total_socios, indice_total=indice_total
        )
    )

