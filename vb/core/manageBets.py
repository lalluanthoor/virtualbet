'''
Created on 30-Apr-2016

@author: lalluanthoor
'''

from ..models import Bet
from django.db.models import Sum
from math import ceil

def getTotalMoney(match):
    return int(Bet.objects.filter(match=match).aggregate(total=Sum('amount'))['total'] if Bet.objects.filter(match=match).aggregate(total=Sum('amount'))['total'] else '0')

def getTotalWinnersBet(match, winTeam):
    return int(Bet.objects.filter(match=match,team=winTeam).aggregate(total=Sum('amount'))['total'] if Bet.objects.filter(match=match,team=winTeam).aggregate(total=Sum('amount'))['total'] else '0')
    
def manageBets(match, winTeam):
    total = getTotalMoney(match)
    totalWinBet = getTotalWinnersBet(match, winTeam)
    winners = Bet.objects.filter(match=match,team=winTeam)
    
    for winner in winners:
        winAmount = ceil((winner.amount*total)/totalWinBet)
        print winAmount
        winner.user.addReward(winAmount)
        winner.user.save()
        winner.save()
