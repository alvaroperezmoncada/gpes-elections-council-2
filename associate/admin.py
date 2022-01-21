from django.contrib import admin

# Register your models here.
from associate.models import Associate


class AssociateAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(Associate, AssociateAdmin)
