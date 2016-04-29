from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginForm, name='login'),
    url(r'^standings/$', views.standings, name='standings'),
    url(r'^bet/$', views.bet, name='bethome'),
    url(r'^logout/', views.logoutForm, name='logout'),
    url(r'^bet/standings/', views.betStandings, name='betstandings')
]