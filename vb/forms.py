from django import forms

from .models import Bet, Result

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