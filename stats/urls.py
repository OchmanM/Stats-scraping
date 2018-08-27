from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name ="index"),
    #127.0.0.1:8000/stats/
    url(r'^player/(?P<player_name>.+)/$', views.player_details, name="player_details"),
    #127.0.0.1:8000/stats/nick
    url(r'^guild/(?P<guild_name>.+)/$', views.guild_details, name="guild_details"),
]