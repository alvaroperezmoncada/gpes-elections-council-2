from django.contrib import admin

# Register your models here.
from ballot.models import Vote, Ballot


class VoteAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


class BallotAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(Vote, VoteAdmin)
admin.site.register(Ballot, BallotAdmin)
