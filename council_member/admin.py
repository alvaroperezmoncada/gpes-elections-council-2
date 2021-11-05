from django.contrib import admin

# Register your models here.
from council_member.models import CouncilMember


class CouncilMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


admin.site.register(CouncilMember, CouncilMemberAdmin)
