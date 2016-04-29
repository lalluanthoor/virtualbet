from django import forms

from .models import Fixture

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
class BetForm(forms.Form):
    fixtures = Fixture.objects.order_by('-match_date')
    fix = [[x.match_number, x] for x in fixtures]
    match = forms.ChoiceField(label="Match", choices=tuple(fix))
    pass