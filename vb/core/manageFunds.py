'''
Created on 01-May-2016

@author: lalluanthoor
'''
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from vb.forms import AddMoneyForm, MultiplierForm, TransferForm
from vb.models import BettingUser, Configuration


def transferFunds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        config = Configuration.objects.get(pk=1)
        if config.allow_transfer:
            fromUser = BettingUser.objects.get(
                username=request.user.username)
            toUser = BettingUser.objects.get(pk=request.POST['to_user'])
            transferAmount = int(request.POST['amount'])
            if transferAmount <= config.max_transfer_amount:
                if toUser.account_balance <= config.max_receiver_amount:
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
                    messages.error(
                        request, 'Cannot transfer funds to user with more than %s virtual cash' % config.max_receiver_amount)
            else:
                messages.error(
                    request, 'Cannot transfer more than %s virtual cash' % config.max_transfer_amount)
        else:
            messages.error(
                request, 'Transfers not allowed at this time. Check back later.')
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
    return HttpResponse(render(request, 'super/addmoney.html', context={'form': form, 'active': {'addmoney': 'active'}, 'title': 'Add Money', 'theme': theme}))


def addLuckyDraw(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        user = BettingUser.objects.get(pk=request.POST['to_user'])
        amount = int(request.POST['amount'])
        user.account_balance += amount
        user.save()
        messages.success(request, 'Lucky Draw Amount Sent')
    else:
        messages.error(request, 'Validation Error')
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'super/luckydraw.html', context={'form': form, 'theme': theme, 'title': 'Lucky Draw', 'active': {'luckydraw': 'active'}}))
