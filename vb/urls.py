from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.loginForm, name='login'),
    url(r'^standings/$', views.standings, name='standings'),
    url(r'^bet/$', views.bet, name='bethome'),
    url(r'^logout/$', views.logoutForm, name='logout'),
    url(r'^bet/standings/$', views.betStandings, name='betstandings'),
    url(r'^bet/placebet/$', views.placeBet, name='placebet'),
    url(r'^bet/super/addresult/$', views.addResult, name='addresult'),
    url(r'^bet/super/$', views.admin, name='adminHome'),
    url(r'^bet/super/standings/$',
        views.adminStandings, name='adminstandings'),
    url(r'^bet/transfer/$', views.transfer, name='transfer'),
    url(r'^bet/super/multiplier/$', views.multiplier, name='multiplier'),
    url(r'^bet/super/config/$', views.config, name='config')
]
