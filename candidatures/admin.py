from django.contrib import admin

# Register your models here.
from candidatures.models import Candidature
from circumscription.models import Circumscription


class CandidatureAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'dni_number', 'circumscription', 'validated', 'is_allegate', 'seniority_date', 'announcement',
        'cuentaVotos'
    )


admin.site.register(Candidature, CandidatureAdmin)
