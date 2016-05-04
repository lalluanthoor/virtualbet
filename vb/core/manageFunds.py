'''
Created on 01-May-2016

@author: lalluanthoor
'''
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from vb.forms import AddMoneyForm

from ..forms import ConfigForm, MultiplierForm, TransferForm
from ..models import BettingUser, Configuration


def transferFunds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        fromUser = BettingUser.objects.get(
            username=request.user.username)
        toUser = BettingUser.objects.get(pk=request.POST['to_user'])
        transferAmount = request.POST['amount']
        if fromUser.account_balance < transferAmount:
            messages.error(request, "Not Enough Money")
        else:
            messages.success(request, "Amount Transferred")
            fromUser.account_balance -= transferAmount
            fromUser.save()
            toUser.account_balance += transferAmount
            toUser.save()
            form = TransferForm()
    else:
        messages.error(request, "Validation Error")
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'bet/transfer.html', context={'form': form, 'active': {'transfer': 'active'}, 'theme': theme}))


def addMultiplier(request):
    form = MultiplierForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, "Multiplier Added")
        except:
            messages.error(request, "Multiplier Already Saved")
    else:
        messages.error(request, "Validation Error")
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'super/multiplier.html', context={'active': {'multiplier': 'active'}, 'form': form, 'theme': theme}))


def addMoney(request):
    form = AddMoneyForm(request.POST)
    if form.is_valid():
        users = BettingUser.objects.filter(bet_admin=False)
        for user in users:
            user.account_balance += int(request.POST['amount'])
            user.save()
            messages.success(request, 'Money Sent to All')
    else:
        messages.error(request, 'Validation Error')
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'super/addmoney.html', context={'form': form, 'active': {'addmoney': 'active'}, 'title': 'Add Money | VirtualBet', 'theme': theme}))
