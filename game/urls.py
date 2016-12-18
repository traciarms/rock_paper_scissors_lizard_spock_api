from django.conf.urls import url

from game import views

urlpatterns = [
    url(r'^games/$', views.GameList.as_view()),
    url(r'^scores/$', views.ListGameScores.as_view()),
    url(r'^start/$', views.ListCreateGame.as_view(), name='start'),
    url(r'^score/(?P<player_name>\w+)/$', views.ScoreDetail.as_view()),
    url(r'^computer_wins/$', views.ComputerWins.as_view()),
]

