from django.shortcuts import render

# Create your views here.
from admin.utils import get_active_modules, commision, edit_candidate, vote
from associate.models import Associate


def index_view(request):
    active_modules = get_active_modules(request)
    if active_modules.count() == 0:
        return render(request, 'deadlines.html')
    return render(request, 'select_module.html', context={'modules': active_modules})


def commision60(request):
    return commision(request, 60)


def commision15(request):
    return commision(request, 15)


def edit_candidate60(request, num):
    return edit_candidate(request, 60, num)


def edit_candidate15(request, num):
    return edit_candidate(request, 15, num)


def vote60(request):
    return vote(request, 60, Associate)
