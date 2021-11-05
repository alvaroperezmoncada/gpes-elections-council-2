from django.contrib import admin

# Register your models here.
from deadlines.models import Deadline


class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'ds', 'module', 'start_dt', 'end_dt')


admin.site.register(Deadline, DeadlineAdmin)
