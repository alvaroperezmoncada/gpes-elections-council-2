from django.shortcuts import render

# Create your views here.
from admin.utils import get_active_modules


def index_view(request):
    active_modules = get_active_modules(request)
    if active_modules.count() == 0:
        return render(request, 'deadlines.html')
    return render(request, 'select_module.html', context={'modules': active_modules})
