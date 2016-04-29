from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import BettingUser, Bet
from .forms import LoginForm
from django.http.response import HttpResponseRedirect

# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/vb/bet/')
    else:
        return HttpResponse(render(request,'user/index.html',context=None))

def loginForm(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/vb/bet/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
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
    if request.user.is_authenticated():
        context = {'bets':Bet.objects.order_by('-match').filter(user=request.user), 'active':{'home':"active"}}
        return HttpResponse( render(request, 'bet/index.html', context=context))
    else:
        return HttpResponseRedirect('/vb/login')

def logoutForm(request):
    logout(request)
    return HttpResponseRedirect('/vb/login')

def betStandings(request):
    if request.user.is_authenticated():
        context = {'users':BettingUser.objects.order_by('-account_balance'),'active':{'standings':"active"}}
        return HttpResponse(render(request, 'bet/standings.html', context))
    else:
        return HttpResponseRedirect('/vb/standings/')
