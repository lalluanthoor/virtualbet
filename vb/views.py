import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, forms
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from vb.forms import ConfigForm, RegistrationForm, AddMoneyForm, PasswordForm

from .core import manageBets, manageCentral, manageFunds
from .forms import ResultForm, LoginForm, BetForm, TransferForm, MultiplierForm
from .models import BettingUser, Bet, Configuration


def index(request):
    print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.user.is_authenticated():
        return HttpResponseRedirect('/bet/')
    else:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        return HttpResponse(render(request, 'user/index.html', context={'title': 'Home', 'theme': theme}))


def loginForm(request):
    if request.user.is_authenticated():
        if not BettingUser.objects.get(username=request.user.username).bet_admin:
            return HttpResponseRedirect('/bet/')
        else:
            return HttpResponseRedirect('/bet/super/')
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
                            return HttpResponseRedirect('/bet/super/')
                        else:
                            return HttpResponseRedirect('/bet/')
                    else:
                        messages.error(request, 'Invalid username/password')
                else:
                    messages.error(request, 'Invalid username/password')
            else:
                messages.error(request, 'Validation Error')
        else:
            form = LoginForm()
        theme = Configuration.objects.get(pk=1).theme.theme_name
        return HttpResponse(render(request, 'user/login.html', context={'form': form, 'title': 'Login', 'theme': theme}))


def changepassword(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            return manageCentral.changePassword(request)
        else:
            form = forms.PasswordChangeForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'bet/changepassword.html', context={'form': form, 'theme': theme, 'title': 'Change Password'}))
    else:
        return HttpResponseRedirect('/login/')


def standings(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('bet/standings.html')
    else:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'users': BettingUser.objects.order_by(
            '-account_balance', 'first_name', 'last_name').filter(bet_admin=False), 'title': 'Standings', 'theme': theme}
        return HttpResponse(render(request, 'user/standings.html', context))


def bet(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'bets': Bet.objects.order_by(
            '-match').filter(user=request.user), 'active': {'home': "active"}, 'title': 'Bet Home', 'theme': theme}
        return HttpResponse(render(request, 'bet/index.html', context=context))
    else:
        return HttpResponseRedirect('/login')


def logoutForm(request):
    logout(request)
    return HttpResponseRedirect('/login')


def betStandings(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'users': BettingUser.objects.order_by(
            '-account_balance', 'first_name', 'last_name').filter(bet_admin=False), 'active': {'standings': "active"}, 'title': 'Standings', 'theme': theme}
        return HttpResponse(render(request, 'bet/standings.html', context))
    else:
        return HttpResponseRedirect('/login/')


def placeBet(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageBets.placeBets(request)
        else:
            form = BetForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'bet/placebet.html', context={'form': form, 'active': {"placebet": "active"}, 'title': 'Bet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/login/')


def admin(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        bets = Bet.objects.order_by('-match')
        theme = Configuration.objects.get(pk=1).theme.theme_name
        return HttpResponse(render(request, 'super/index.html', context={'active': {'home': 'active'}, 'bets': bets, 'title': 'Admin Home | Virtual Bet', 'theme': theme}))
    else:
        return HttpResponseRedirect('/login')


def addResult(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageBets.addResult(request)
        else:
            form = ResultForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/addresult.html', context={'active': {'addresult': 'active'}, 'form': form, 'title': 'Add Result', 'theme': theme}))
    else:
        return HttpResponseRedirect('/login')


def adminStandings(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        theme = Configuration.objects.get(pk=1).theme.theme_name
        context = {'users': BettingUser.objects.order_by(
            '-account_balance', 'first_name', 'last_name').filter(bet_admin=False), 'active': {'standings': "active"}, 'title': 'Standings', 'theme': theme}
        return HttpResponse(render(request, 'super/standings.html', context))
    else:
        return HttpResponseRedirect('/login/')


def transfer(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.transferFunds(request)
        else:
            form = TransferForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'bet/transfer.html', context={'form': form, 'active': {'transfer': 'active'}, 'title': 'Transfers', 'theme': theme}))
    else:
        return HttpResponseRedirect('/login/')


def multiplier(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.addMultiplier(request)
        else:
            form = MultiplierForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/multiplier.html', context={'form': form, 'active': {'multiplier': 'active'}, 'title': 'Win Multiplier', 'theme': theme}))
    else:
        return HttpResponseRedirect('/login/')


def config(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageCentral.configUpdate(request)
        else:
            form = ConfigForm(instance=Configuration.objects.get(pk=1))
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/config.html', context={'form': form, 'active': {'config': 'active'}, 'title': 'Configuration', 'theme': theme}))
    else:
        return HttpResponseRedirect('/login/')


def addmoney(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.addMoney(request)
        else:
            form = AddMoneyForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/addmoney.html', context={'form': form, 'active': {'addmoney': 'active'}, 'title': 'Add Money', 'theme': theme}))
    else:
        HttpResponseRedirect('/login/')


def register(request):
    if request.method == 'POST':
        return manageCentral.registerUser(request)
    else:
        form = RegistrationForm()
        theme = Configuration.objects.get(pk=1).theme.theme_name
        return HttpResponse(render(request, 'user/registration.html', context={'form': form, 'theme': theme, 'title': 'Register'}))


def luckydraw(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username=request.user.username).bet_admin:
        if request.method == 'POST':
            return manageFunds.addLuckyDraw(request)
        else:
            form = TransferForm()
            theme = Configuration.objects.get(pk=1).theme.theme_name
            return HttpResponse(render(request, 'super/luckydraw.html', context={'form': form, 'theme': theme, 'title': 'Lucky Draw', 'active': {'luckydraw': 'active'}}))
    else:
        HttpResponseRedirect('/login')
