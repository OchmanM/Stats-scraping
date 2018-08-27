from django.shortcuts import render, redirect
from .models import Player, Deaths
from functools import reduce
from queryset_sequence import QuerySetSequence
from django.http import HttpResponse
# Create your views here.


def index(request):
    deaths = Deaths.objects.all().order_by('-date')[:200]
    return render(request, 'index.html', {'deaths':deaths })


def player_details(request, player_name):
    player = Player.objects.get(name=player_name)
    deaths = Deaths.objects.filter(killed=player)
    return render(request, 'player.html', {'player': player, 'deaths': deaths })


def guild_details(request, guild_name):
    players = Player.objects.filter(guild=guild_name)
    deaths = reduce(QuerySetSequence,[Deaths.objects.filter(killed=player) for player in players])
    kills = reduce(QuerySetSequence,[Deaths.objects.filter(killer=player) for player in players])
    return render(request, 'guild.html', {'players': players,
                                          'deaths': deaths,
                                          'kills': kills,
                                          'guild_name': guild_name}
                  )