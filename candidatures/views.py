from django.shortcuts import render

from candidatures.utils import presentation, confirm


def presentation60_view(request):
    return presentation(request, 60)


def presentation_15(request):
    return True


def confirm60_view(request):
    return confirm(request, 60)


def ok60(request):
    return render(request, 'ok_60.html')
