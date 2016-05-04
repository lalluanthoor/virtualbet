from django.contrib import admin

from vb.models import Bet, BettingUser, Configuration, Fixture, Result, Team, Theme, WinMultiplier


# Register your models here.
admin.site.register(Bet)
admin.site.register(BettingUser)
admin.site.register(Configuration)
admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(Team)
admin.site.register(Theme)
admin.site.register(WinMultiplier)
