from django.contrib import admin

# Register your models here.
from council_member.models import CouncilMember


class CouncilMemberAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dni_number', 'email')


admin.site.register(CouncilMember, CouncilMemberAdmin)
