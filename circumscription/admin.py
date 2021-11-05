from django.contrib import admin

# Register your models here.
from circumscription.models import Circumscription


class CircumscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ds', 'alize', 'cod_ine', 'places', 'order')


admin.site.register(Circumscription, CircumscriptionAdmin)
