'''
@author: lalluanthoor
'''
from datetime import date
from django import forms

from vb.models import BettingUser, Configuration, Fixture
from vb.models import Result, Team, WinMultiplier


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class BetForm(forms.Form):
    matches = [[x.pk, x.__str__()]
               for x in Fixture.objects.order_by('match_number').filter(match_date__gte=date.today())]
    match = forms.ChoiceField(choices=matches)
    teams = [[x.pk, x.__str__()] for x in Team.objects.all()]
    team = forms.ChoiceField(choices=teams)
    amount = forms.IntegerField(min_value=1)


class ResultForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = '__all__'


class TransferForm(forms.Form):
    data = [[x.pk, x.first_name.title() + ' ' + x.last_name.title()]
            for x in BettingUser.objects.filter(bet_admin=False).order_by('first_name', 'last_name')]
    to_user = forms.ChoiceField(choices=data, label='To User')
    amount = forms.IntegerField(min_value=1)


class MultiplierForm(forms.ModelForm):

    class Meta:
        model = WinMultiplier
        fields = '__all__'


class ConfigForm(forms.ModelForm):

    class Meta:
        model = Configuration
        fields = '__all__'


class AddMoneyForm(forms.Form):
    amount = forms.IntegerField(min_value=1)


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = BettingUser
        fields = ['username', 'first_name',
                  'last_name', 'email', 'password']
