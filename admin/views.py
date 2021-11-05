from django.shortcuts import render

# Create your views here.
from admin.utils import get_active_modules


def index_view(request):
    return render(request, 'select_module.html', context={'modules': get_active_modules(request)})
