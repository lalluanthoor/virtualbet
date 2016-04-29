from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Team( models.Model ):
    team_name = models.CharField(max_length=200)
    team_abbr = models.CharField(max_length=3)
    
    def __str__(self):
        return self.team_name
    
class Fixture( models.Model ):
    home_team = models.ForeignKey( Team, on_delete=models.CASCADE, related_name='home_team' )
    away_team = models.ForeignKey( Team, on_delete=models.CASCADE, related_name='away_team' )
    match_date = models.DateField()
    match_time = models.TimeField()
    match_number = models.IntegerField(default=1)
    
    def __str__(self):
        return 'Match ' + str(self.match_number) + ' : ' + self.home_team.team_abbr + ' vs ' + self.away_team.team_abbr
    
class Result( models.Model ):
    match = models.ForeignKey( Fixture, on_delete=models.CASCADE )
    winning_team = models.ForeignKey( Team, on_delete=models.CASCADE )
    
    def __str__(self):
        return self.match.__str__() + ' won by ' + self.winning_team
    
class BettingUser( User ):
    account_balance = models.IntegerField()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def placeBet(self, amount):
        self.account_balance -= amount
        
    def addReward(self, amount):
        self.account_balance += amount

class Bet( models.Model ):
    match = models.ForeignKey( Fixture, on_delete=models.CASCADE )
    user = models.ForeignKey( BettingUser, on_delete=models.CASCADE )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default='1')
    amount = models.IntegerField()
    
    def __str__(self):
        return self.user.__str__() + ' bet ' + str(self.amount) + ' on ' + self.match.__str__() 
