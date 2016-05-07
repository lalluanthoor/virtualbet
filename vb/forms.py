from datetime import date

from django import forms

from vb.models import Fixture

from .models import Bet, Result, Configuration, BettingUser, WinMultiplier


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)


class BetForm(forms.ModelForm):
    matches = Fixture.objects.filter(match_date >= date.today())
    match = forms.ChoiceField(choices=matches, label='New Match')

    class Meta:
        model = Bet
        exclude = ['user']


class ResultForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = '__all__'


class TransferForm(forms.Form):
    data = [[x.pk, x.first_name.title() + ' ' + x.last_name.title()]
            for x in BettingUser.objects.filter(bet_admin=False)]
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
