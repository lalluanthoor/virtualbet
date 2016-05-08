'''
@author: lalluanthoor
'''
from datetime import datetime, timedelta, tzinfo
from math import ceil

from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse
from django.shortcuts import render

from vb.forms import BetForm, ResultForm
from vb.models import Bet, BettingUser, Configuration, Fixture, Team, WinMultiplier


ZERO = timedelta(0)


class FixedOffset(tzinfo):

    def __init__(self, offset, name):
        self.__offset = timedelta(minutes=offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO


def getTotalLosersBet(match, winTeam):
    return int(Bet.objects.filter(~Q(team=winTeam), match=match).aggregate(total=Sum('amount'))['total'] if Bet.objects.filter(match=match).aggregate(total=Sum('amount'))['total'] else '0')


def getTotalWinnersBet(match, winTeam):
    return int(Bet.objects.filter(match=match, team=winTeam).aggregate(total=Sum('amount'))['total'] if Bet.objects.filter(match=match, team=winTeam).aggregate(total=Sum('amount'))['total'] else '0')


def manageBets(match, winTeam):
    totalLosersBet = getTotalLosersBet(match, winTeam)
    totalWinBet = getTotalWinnersBet(match, winTeam)
    winners = Bet.objects.filter(match=match, team=winTeam)
    multiply = WinMultiplier.objects.filter(match=match, team=winTeam)
    multiplier = 1 if multiply is None else multiply[0].multiplier

    for winner in winners:
        winAmount = winner.amount + \
            ceil((winner.amount * totalLosersBet * multiplier) / totalWinBet)
        winner.user.addReward(winAmount)
        winner.user.save()
        winner.save()


def placeBets(request):
    form = BetForm(request.POST)
    if form.is_valid():
        try:
            _now = datetime.strftime(
                datetime.now(FixedOffset(330, 'IST')), '%Y-%m-%d %H:%M:%S')
            _match = str(Fixture.objects.get(
                pk=request.POST['match']).match_date) + ' ' + str(Fixture.objects.get(
                    pk=request.POST['match']).match_time)
            _t1 = datetime.strptime(_now, '%Y-%m-%d %H:%M:%S')
            _t2 = datetime.strptime(_match, '%Y-%m-%d %H:%M:%S')
            _delta = _t1 - _t2
            _allowed = timedelta(
                minutes=Configuration.objects.get(pk=1).getTime())
            if _delta > _allowed:
                raise Exception("Cannot Bet Now, Time Expired")
            bet = Bet()
            bet.match = Fixture.objects.get(pk=request.POST['match'])
            bet.team = Team.objects.get(pk=request.POST['team'])
            bet.amount = int(request.POST['amount'])
            bet.user = BettingUser.objects.get(username=request.user)
            if bet.user.account_balance < bet.amount:
                raise Exception("Not Enough Money")
            bet.user.placeBet(int(bet.amount))
            if bet.team != bet.match.home_team and bet.team != bet.match.away_team:
                raise Exception("Please Bet on Playing Team")
            bet.save()
            bet.user.save()
            messages.success(request, "Bet Placed")
            form = BetForm()
        except Exception as e:
            if e.message.startswith('UNIQUE'):
                msg = "Bet Already Placed"
            else:
                msg = e.message
            messages.error(request, msg)
    else:
        messages.error(request, "Validation Error")
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'bet/placebet.html', context={'form': form, 'active': {"placebet": "active"}, 'theme': theme}))


def addResult(request):
    form = ResultForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            manageBets(request.POST[u'match'], request.POST[u'winning_team'])
            messages.success(request, "Result Saved")
        except Exception as e:
            messages.error(request, e.message)
    else:
        messages.error(request, "Validation Error")
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'super/addresult.html', context={'active': {'addresult': 'active'}, 'form': form, 'theme': theme}))
