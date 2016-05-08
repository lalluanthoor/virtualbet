'''
Created on 03-May-2016

@author: lalluanthoor
'''

from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render

from vb.forms import ConfigForm, RegistrationForm, PasswordForm
from vb.models import Configuration, BettingUser


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
    form = PasswordForm(request.POST)
    returnTemplate = 'super/changepassword.html' if BettingUser.objects.get(
        username=request.user.username).bet_admin else 'bet/changepassword.html'
    if form.is_valid():
        username = request.user.username
        password = request.POST['old_password']
        user = authenticate(username, password)
        if user is None:
            messages.error(request, 'Current password is wrong')
        else:
            npassword = request.POST['new_password']
            cpassword = request.POST['confirm_password']
            if npassword != cpassword:
                messages.error(request, 'Passwords do not match')
            else:
                user = BettingUser.objects.get(username=username)
                user.set_password(npassword)
                user.save()
                form = PasswordForm()
                messages.success(request, 'Password changed')
    else:
        messages.error(request, 'Validation Error')
    theme = Configuration.objects.get(pk=1).theme.theme_name
    return HttpResponse(render(request, returnTemplate, context={'form': form, 'theme': theme, 'title': 'Change Password'}))
