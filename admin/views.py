from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from admin.utils import detalle_prueba, get_active_modules, commision, edit_candidate, vote, send_pass, ballot, register_vote, selector, \
    results
from associate.models import Associate
from council_member.models import CouncilMember
from deadlines.models import Deadline


def index_view(request):
    active_modules = get_active_modules(request)
    if active_modules.count() > 0:
        return render(request, 'index.html', context={'modules': active_modules})
    return render(request, 'deadlines.html', context={'modules': Deadline.objects.all()})


@login_required
def commision60(request):
    return commision(request, 60)


@login_required
def commision15(request):
    return commision(request, 15)


@login_required
def edit_candidate60(request, num):
    return edit_candidate(request, 60, num)


@login_required
def edit_candidate15(request, num):
    return edit_candidate(request, 15, num)


def vote60(request):
    return vote(request, 60, Associate)


def vote15(request):
    return vote(request, 15, CouncilMember)


def send_pass60(request):
    return send_pass(request, 60)


def send_pass15(request):
    return send_pass(request, 15)


def ballot60(request, ca):
    return ballot(request, ca, 60, Associate)


def ballot15(request, ca):
    return ballot(request, ca, 15, CouncilMember)


def register_vote60(request, ca):
    return register_vote(request, ca, 60, Associate)


def register_vote15(request, ca):
    return register_vote(request, ca, 15, CouncilMember)


def results60(request):
    return results(request, 60)


def results15(request):
    return results(request, 15)


@login_required
def selector60(request):
    return selector(request, 60)


@login_required
def selector15(request):
    return selector(request, 15)

@login_required
def detalles(request, path):
    print(path)
    return detalle_prueba(request)