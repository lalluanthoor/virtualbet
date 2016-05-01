from django import forms

from .models import Bet, Result,BettingUser

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        exclude = ['user']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'

class TransferForm(forms.Form):
    to_user = forms.ChoiceField(choices=[[x.pk, x.first_name+' '+x.last_name] for x in BettingUser.objects.filter(bet_admin=False)])
    amount = forms.IntegerField(min_value=1)
