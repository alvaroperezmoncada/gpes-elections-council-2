from django.contrib import admin

# Register your models here.
from provinces.models import Province


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'ds', 'circumscription', 'prefix_cp')


admin.site.register(Province, ProvinceAdmin)
