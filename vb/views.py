from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import BettingUser, Bet
from .forms import LoginForm, BetForm
from django.http.response import HttpResponseRedirect
from vb.forms import ResultForm
from .core import manageBets

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/vb/bet/')
    else:
        return HttpResponse(render(request,'user/index.html',context=None))

def loginForm(request):
    if request.user.is_authenticated():
        if not BettingUser.objects.get(username = request.user.username).bet_admin:
            return HttpResponseRedirect('/vb/bet/')
        else:
            return HttpResponseRedirect('/vb/bet/super/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
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
            return HttpResponse( render(request, 'user/login.html', context={'form':form}))

def standings(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('bet/standings.html')
    else:
        context = { 'users' : BettingUser.objects.order_by('-account_balance') }
        return HttpResponse( render(request, 'user/standings.html', context))

def bet(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username = request.user.username).bet_admin:
        context = {'bets':Bet.objects.order_by('-match').filter(user=request.user), 'active':{'home':"active"}}
        return HttpResponse( render(request, 'bet/index.html', context=context))
    else:
        return HttpResponseRedirect('/vb/login')

def logoutForm(request):
    logout(request)
    return HttpResponseRedirect('/vb/login')

def betStandings(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username = request.user.username).bet_admin:
        context = {'users':BettingUser.objects.order_by('-account_balance'),'active':{'standings':"active"}}
        return HttpResponse(render(request, 'bet/standings.html', context))
    else:
        return HttpResponseRedirect('/vb/standings/')
    
def placeBet(request):
    if request.user.is_authenticated() and not BettingUser.objects.get(username = request.user.username).bet_admin:
        if request.method == 'POST':
            form = BetForm(request.POST)
            if form.is_valid():
                try:
                    bet = form.save(commit=False)
                    bet.user = BettingUser.objects.get(username = request.user)
                    if bet.user.account_balance < bet.amount:
                        raise Exception("Not Enough Money")
                    bet.user.placeBet(int(bet.amount))
                    if bet.team != bet.match.home_team and bet.team != bet.match.away_team:
                        raise Exception("Please Bet on Playing Team")
                    bet.save()
                    bet.user.save()
                    messages.success(request, "Bet Placed")
                    context = {'bets':Bet.objects.order_by('-match').filter(user=request.user), 'active':{'home':"active"}}
                    return HttpResponse(render(request,'bet/index.html',context=context))
                except Exception as e:
                    if e.message.startswith('UNIQUE'):
                        msg = "Bet Already Placed"
                    else:
                        msg = e.message
                    messages.error(request, msg)
                    return HttpResponse(render(request,'bet/placebet.html', context={'form':form, 'active':{'placebet':'active'}}))
            else:
                messages.error(request, "Validation Error")
                return HttpResponse( render(request, 'bet/placebet.html', context={'form':form, 'active':{"placebet":"active"}}) )
        else:
            form = BetForm()
            return HttpResponse( render(request, 'bet/placebet.html', context={'form':form, 'active':{"placebet":"active"}}) )
    else:
        return HttpResponseRedirect('/vb/login/')
    
def admin(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username = request.user.username).bet_admin:
        bets = Bet.objects.order_by('-match')
        return HttpResponse(render(request, 'super/index.html', context={'active':{'home':'active'},'bets':bets}))
    else:
        return HttpResponseRedirect('/vb/')
    
def addResult(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username = request.user.username).bet_admin:
        if request.method == 'POST':
            form = ResultForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                    manageBets.manageBets(request.POST[u'match'], request.POST[u'winning_team'])
                    messages.success(request, "Result Saved")
                    return HttpResponse(render(request, 'super/addresult.html', context={'active':{'addresult':'active'}, 'form':form}))
                except Exception as e:
                    print e
                    messages.error(request, "Result Already Saved")
                    return HttpResponse(render(request, 'super/addresult.html', context={'active':{'addresult':'active'}, 'form':form}))
            else:
                messages.error(request, "Validation Error")
                return HttpResponse(render(request, 'super/addresult.html', context={'active':{'addresult':'active'}, 'form':form}))
        else:
            form = ResultForm()
            return HttpResponse(render(request, 'super/addresult.html', context={'active':{'addresult':'active'}, 'form':form}))
    else:
        return HttpResponseRedirect('/vb/login')
    
def adminStandings(request):
    if request.user.is_authenticated() and BettingUser.objects.get(username = request.user.username).bet_admin:
        context = {'users':BettingUser.objects.order_by('-account_balance').filter(bet_admin=False),'active':{'standings':"active"}}
        return HttpResponse(render(request, 'super/standings.html', context))
    else:
        return HttpResponseRedirect('/vb/login/')
