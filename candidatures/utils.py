from django.shortcuts import render

from candidatures.forms import NewCandidature


def presentation(request, _type):
    form = NewCandidature()
    return render(request, 'presentation.html', {'form': form})
