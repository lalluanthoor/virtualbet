from django.contrib import admin
from .models import Bet, BettingUser, Fixture, Result, Team
# Register your models here.

admin.site.register(Bet)
admin.site.register(BettingUser)
admin.site.register(Fixture)
admin.site.register(Result)
admin.site.register(Team)
