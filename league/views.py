from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.core import exceptions

from .models import *
from .forms import *

def index(request):
    seasons = Season.objects.filter(season_active=True)
    return render(request, "league/index.html", {"seasons": seasons})

def season(request, season_slug, gpage=1, rpage=1):
    season = get_object_or_404(Season, season_slug=season_slug)
    game_paginator = Paginator(Game.objects.filter(season_id=season).order_by("game_date"), 10)
    page_obj = game_paginator.get_page(request.GET.get("gpage"))
    rank_paginator = Paginator(Rank.objects.filter(season_id=season).order_by("score"), 10)
    rank_obj = rank_paginator.get_page(request.GET.get("rpage"))
    context =  {
        "season": season,
        "games": page_obj,
        "ranks": rank_obj,
        "season_type": Season.GameTypes(season.season_type)
        }
    return render(request, "league/season.html", context)

def game(request, game_id, season_slug):
    game = get_object_or_404(Game, pk=game_id)
    season = get_object_or_404(Season, season_slug=season_slug)
    return render(request, "league/game.html", {"game": game, "season": season})

def player(request, player_name, season_slug=None):
    player = get_object_or_404(Player, pk=player_name)
    season = get_object_or_404(Season, season_slug=season_slug)
    return render(request, "league/player.html", {"player": player, "season": season})

def add_game(request, season_slug):
    season = get_object_or_404(Season, season_slug=season_slug)

    playerFormSet = formset_factory(
        addPlayerForm, formset=BasePlayerFormSet, extra=season.season_type,
        min_num=season.season_type, validate_min=True,
        max_num=season.season_type, validate_max=True
        )

    if request.method == "POST":
        gameForm = addGameForm(request.POST)
        playerSet = playerFormSet(request.POST)
        playerSet.season = season
        if gameForm.is_valid() and playerSet.is_valid():
            game = Game.objects.create(
                season_id = season, game_notes = gameForm.cleaned_data.get("gameNote")
            )
            scores = []
            for player in playerSet:
                scores.append(
                    {
                        "score": player.cleaned_data.get("endPoints"), 
                        "player": Player.objects.get_or_create(player_name = player.cleaned_data.get("playerName"))[0]
                    }
                )
            # scores = sorted(scores, key=lambda d: d['score'])

            if season.season_type is season.GameTypes.riichi:
                uma_spread = [season.uma_big, season.uma_small, -season.uma_small, -season.uma_big]
            elif season.season_type is season.GameTypes.sanma:
                uma_spread = [season.uma_big, 0, season.uma_small]

            for scoreAndPlayer in scores:
                place=1
                tied=1
                for i in scores:
                    if i is scoreAndPlayer:
                        continue
                    elif i.get("score") > scoreAndPlayer.get("score"):
                        place += 1
                    elif i.get("score") == scoreAndPlayer.get("score"):
                        tied += 1
                uma = sum([uma_spread][place-1:][:tied])/tied


                player_score = (scoreAndPlayer.get("score") - season.season_starting_points)/1000 + season.season_oka + uma

                Score.objects.create(
                    player_name = scoreAndPlayer.get("player"),
                    game_id = game,
                    score_final = scoreAndPlayer.get("score"),
                    score_position = Score.ScorePositions(place),
                    score_uma = uma,
                    score_impact = player_score
                )

                rank, created = Rank.objects.get_or_create(
                    player_name = scoreAndPlayer.get("player"),
                    season_id = season
                )
                rank.score = rank.score + player_score
                rank.save()

            messages.success(request, "Added game")
            return redirect(reverse('league:season', kwargs={"season_slug": season_slug}))
        
    else:
        gameForm = addGameForm()
        playerSet = playerFormSet()

    context =  {
        "season": season,
        "gameForm": gameForm,
        "playerSet": playerSet
        }
    return render(request, "league/add_game.html", context)