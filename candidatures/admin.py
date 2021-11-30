from django.contrib import admin

# Register your models here.
from candidatures.models import Candidature
from circumscription.models import Circumscription


class CandidatureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'circumscription', 'validated', 'seniority_date', 'announcement')


admin.site.register(Candidature, CandidatureAdmin)
