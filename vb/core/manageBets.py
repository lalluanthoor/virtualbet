'''
Created on 30-Apr-2016

@author: lalluanthoor
'''
from math import ceil

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render

from ..forms import BetForm, ResultForm
from ..models import Bet, BettingUser, WinMultiplier


def getTotalMoney(match):
    return int(Bet.objects.filter(match=match).aggregate(total=Sum('amount'))['total'] if Bet.objects.filter(match=match).aggregate(total=Sum('amount'))['total'] else '0')


def getTotalWinnersBet(match, winTeam):
    return int(Bet.objects.filter(match=match, team=winTeam).aggregate(total=Sum('amount'))['total'] if Bet.objects.filter(match=match, team=winTeam).aggregate(total=Sum('amount'))['total'] else '0')


def manageBets(match, winTeam):
    total = getTotalMoney(match)
    totalWinBet = getTotalWinnersBet(match, winTeam)
    winners = Bet.objects.filter(match=match, team=winTeam)
    multiply = WinMultiplier.objects.filter(match=match, team=winTeam)
    multiplier = 1 if multiply is None else multiply.multiplier

    for winner in winners:
        winAmount = ceil((winner.amount * total * multiplier) / totalWinBet)
        winner.user.addReward(winAmount)
        winner.user.save()
        winner.save()


def placeBets(request):
    form = BetForm(request.POST)
    if form.is_valid():
        try:
            bet = form.save(commit=False)
            bet.user = BettingUser.objects.get(username=request.user)
            if bet.user.account_balance < bet.amount:
                raise Exception("Not Enough Money")
            bet.user.placeBet(int(bet.amount))
            if bet.team != bet.match.home_team and bet.team != bet.match.away_team:
                raise Exception("Please Bet on Playing Team")
            bet.save()
            bet.user.save()
            messages.success(request, "Bet Placed")
            context = {'bets': Bet.objects.order_by(
                '-match').filter(user=request.user), 'active': {'home': "active"}}
            return HttpResponse(render(request, 'bet/index.html', context=context))
        except Exception as e:
            if e.message.startswith('UNIQUE'):
                msg = "Bet Already Placed"
            else:
                msg = e.message
            messages.error(request, msg)
            return HttpResponse(render(request, 'bet/placebet.html', context={'form': form, 'active': {'placebet': 'active'}}))
    else:
        messages.error(request, "Validation Error")
        return HttpResponse(render(request, 'bet/placebet.html', context={'form': form, 'active': {"placebet": "active"}}))


def addResult(request):
    form = ResultForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            manageBets(request.POST[u'match'], request.POST[u'winning_team'])
            messages.success(request, "Result Saved")
            return HttpResponse(render(request, 'super/addresult.html', context={'active': {'addresult': 'active'}, 'form': form}))
        except Exception as e:
            print e
            messages.error(request, "Result Already Saved")
            return HttpResponse(render(request, 'super/addresult.html', context={'active': {'addresult': 'active'}, 'form': form}))
    else:
        messages.error(request, "Validation Error")
        return HttpResponse(render(request, 'super/addresult.html', context={'active': {'addresult': 'active'}, 'form': form}))
