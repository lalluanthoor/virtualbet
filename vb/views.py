from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from vb.forms import ConfigForm

from .core import manageBets, manageFunds
from .forms import ResultForm, LoginForm, BetForm, TransferForm, MultiplierForm
from .models import BettingUser, Bet, Configuration


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/vb/bet/')
    else:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        return HttpResponse(render(request, 'user/index.html', context={'title': 'Home | VirtualBet', 'theme': theme}))


def loginForm(request):
    if request.user.is_authenticated():
        if not BettingUser.objects.get(username=request.user.username).bet_admin:
            return HttpResponseRedirect('/vb/bet/')
        else:
            return HttpResponseRedirect('/vb/bet/super/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        usr = BettingUser.objects.get(username=user.username)
                        login(request, user)
                        if usr.bet_admin:
                            return HttpResponseRedirect('/vb/bet/super/')
                        else:
                            return HttpResponseRedirect('/vb/bet/')
                    else:
                        return HttpResponseRedirect('/vb/login/')
                else:
                    return HttpResponseRedirect('/vb/login/')
        else:
            form = LoginForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'user/login.html', context={'form': form, 'title': 'Login | VirtualBet', 'theme': theme}))


def standings(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('bet/standings.html')
    else:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'users': BettingUser.objects.order_by(
            '-account_balance').filter(bet_admin=False), 'title': 'Standings | VirtualBet', 'theme': theme}
        return HttpResponse(render(request, 'user/standings.html', context))


def bet(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'bets': Bet.objects.order_by(
            '-match').filter(user=request.user), 'active': {'home': "active"}, 'title': 'Bet Home | VirtualBet', 'theme': theme}
        return HttpResponse(render(request, 'bet/index.html', context=context))
    else:
        return HttpResponseRedirect('/vb/login')


def logoutForm(request):
    logout(request)
    return HttpResponseRedirect('/vb/login')


def betStandings(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'users': BettingUser.objects.order_by(
            '-account_balance').filter(bet_admin=False), 'active': {'standings': "active"}, 'title': 'Standings | VirtualBet', 'theme': theme}
        return HttpResponse(render(request, 'bet/standings.html', context))
    else:
        return HttpResponseRedirect('/vb/standings/')


def placeBet(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageBets.placeBets(request)
        else:
            form = BetForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'bet/placebet.html', context={'form': form, 'active': {"placebet": "active"}, 'title': 'Bet | VirtualBet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/vb/login/')


def admin(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        bets = Bet.objects.order_by('-match')
        theme = Configuration.objects.get(pk=1).theme.theme_name
        return HttpResponse(render(request, 'super/index.html', context={'active': {'home': 'active'}, 'bets': bets, 'title': 'Admin Home | Virtual Bet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/vb/')


def addResult(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            manageBets.addResult(request)
        else:
            form = ResultForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/addresult.html', context={'active': {'addresult': 'active'}, 'form': form, 'title': 'Add Result | VirtualBet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/vb/login')


def adminStandings(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'users': BettingUser.objects.order_by(
            '-account_balance').filter(bet_admin=False), 'active': {'standings': "active"}, 'title': 'Standings | VirtualBet', 'theme': theme}
        return HttpResponse(render(request, 'super/standings.html', context))
    else:
        return HttpResponseRedirect('/vb/login/')


def transfer(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.transferFunds(request)
        else:
            form = TransferForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'bet/transfer.html', context={'form': form, 'active': {'transfer': 'active'}, 'title': 'Transfers | VirtualBet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/vb/login/')


def multiplier(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.addMultiplier(request)
        else:
            form = MultiplierForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/multiplier.html', context={'form': form, 'active': {'multiplier': 'active'}, 'title': 'Win Multiplier | VirtualBet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/vb/login/')


def config(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.configUpdate(request)
        else:
            form = ConfigForm(instance=Configuration.objects.get(pk=1))
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/config.html', context={'form': form, 'active': {'config': 'active'}, 'title': 'Configuration | VirtualBet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/vb/login/')
