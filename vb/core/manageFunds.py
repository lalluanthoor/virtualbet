'''
Created on 01-May-2016

@author: lalluanthoor
'''
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from ..forms import ConfigForm, MultiplierForm, TransferForm
from ..models import BettingUser


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
    return HttpResponse(render(request, 'bet/transfer.html', context={'form': form, 'active': {'transfer': 'active'}}))


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
    return HttpResponse(render(request, 'super/multiplier.html', context={'active': {'multiplier': 'active'}, 'form': form}))


def configUpdate(request):
    form = ConfigForm(request.POST)
    if form.is_valid():
        messages.success(request, "Configuration Saved")
    else:
        messages.error(request, "Validation Error")
    return HttpResponse(render(request, 'super/config.html', context={'form': form, 'title': 'Configuration | VirtualBet', 'active': {'config': 'active'}}))
