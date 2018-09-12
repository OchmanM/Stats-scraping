from django.shortcuts import render, redirect
from .models import Player, Deaths
from datetime import datetime, timedelta
import urllib


# Create your views here.



def index(request):
    deaths = Deaths.objects.all().order_by('-date')[:1000]
    return render(request, 'index.html', {'deaths': deaths})


def player_details(request, player_name):
    fixed_player_name = urllib.parse.unquote(player_name)
    player = Player.objects.get(name=fixed_player_name)
    deaths = Deaths.objects.filter(killed=player).order_by('-date')
    kills = Deaths.objects.filter(killer=player).order_by('-date')
    return render(request, 'player.html', {'player': player,
                                           'deaths': deaths,
                                           'kills': kills})


def guild_details(request, guild_name):
    fixed_guild_name = urllib.parse.unquote(guild_name)
    players = Player.objects.filter(guild=fixed_guild_name)
    last_month = datetime.today() - timedelta(days=30)
    deaths = Deaths.objects.filter(killed__in=players, date__gte=last_month).order_by('-date')
    kills = Deaths.objects.filter(killer__in=players, date__gte=last_month).order_by('-date')

    return render(request, 'guild.html', {'players': players,
                                          'deaths': deaths,
                                          'kills': kills,
                                          'guild_name': guild_name})
