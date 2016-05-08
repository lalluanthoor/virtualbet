'''
@author: lalluanthoor
'''

from django.contrib import messages
from django.contrib.auth import forms, update_session_auth_hash
from django.http import HttpResponse
from django.shortcuts import render

from vb.forms import ConfigForm, RegistrationForm
from vb.models import BettingUser, Configuration


def configUpdate(request):
    try:
        conf = Configuration.objects.get(pk=1)
    except:
        conf = Configuration()
    form = ConfigForm(request.POST, instance=conf)
    if form.is_valid():
        form.save()
        messages.success(request, "Configuration Saved")
    else:
        messages.error(request, "Validation Error")
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'super/config.html', context={'form': form, 'title': 'Configuration', 'active': {'config': 'active'}, 'theme': theme}))


def registerUser(request):
    form = RegistrationForm(request.POST)
    usr = form.save(commit=False)
    usr.bet_admin = False
    usr.account_balance = 50000
    usr.is_active = True
    usr.is_staff = False
    usr.is_superuser = False
    usr.set_password(request.POST['password'])
    usr.save()
    form = RegistrationForm()
    messages.success(request, 'Registration Completed')
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, 'user/registration.html', context={'form': form, 'theme': theme, 'title': 'Register'}))


def changePassword(request):
    form = forms.PasswordChangeForm(user=request.user, data=request.POST)
    returnTemplate = 'super/changepassword.html' if BettingUser.objects.get(
        username=request.user.username).bet_admin else 'bet/changepassword.html'
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Passowrd changed')
    else:
        messages.error(request, 'Validation Error')
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, returnTemplate, context={'form': form, 'theme': theme, 'title': 'Change Password'}))
