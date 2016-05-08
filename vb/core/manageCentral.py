'''
Created on 03-May-2016

@author: lalluanthoor
'''

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from vb.forms import ConfigForm, RegistrationForm
from vb.models import Configuration


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
