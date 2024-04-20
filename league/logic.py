from .models import *
from django.db import models

def calculate_scores(game: Game, season: Season, scores: list, uma_spread: list):
    for scoreAndPlayer in scores:

        '''
        Logic for determining placement order

        We could just use sorted(scores, key=lambda d: d['score']) to sort the list by score,
        but then we'd need to run between 1 and 3 comparisons to check for ties (6-12 in total?)
        and add some additional logic to figure out which ones to run.
        So, more code and more complex code.

        Instead, we calculate each player's placement seperately (by comparing them against the three other players)
        and reducing their score (1->2->3->4) each time we find someone who performed better than them.
        We also track how many players they're tied with.

        To calculate the uma, we then slice the uma_spread array to get the relevant uma,
        and divide them by the number of players they're shared between.
        '''
        place=1
        tied=1
        for i in scores:
            if i is scoreAndPlayer:
                continue
            elif i.get("score") > scoreAndPlayer.get("score"):
                place += 1
            elif i.get("score") == scoreAndPlayer.get("score"):
                tied += 1
        uma = sum(uma_spread[place-1:][:tied])/tied

        '''
        Calculate the individual score, and then store the player's placement in the database
        '''
        player_score = (scoreAndPlayer.get("score") - season.starting_points)/1000 + season.oka + uma - scoreAndPlayer.get("penalty")

        score = Score.objects.create(
            player_name = scoreAndPlayer.get("player"),
            game_id = game,
            score_final = scoreAndPlayer.get("score"),
            score_position = Score.ScorePositions(place),
            score_penalty = scoreAndPlayer.get("penalty"),
            score_uma = uma,
            score_impact = player_score
        )

        '''
        Calculate overall league performance, using whichever score calculation method the season is set to use
        '''
        rank, created = Rank.objects.get_or_create(
            player_name = scoreAndPlayer.get("player"),
            season_id = season
        )

        rank.score = calculate_rank(score, season)

        rank.save()

def calculate_rank(score: Score, season: Season):
    scoring = Season.ScoringTypes(season.scoring)
    # if scoring is Season.ScoringTypes.cumulative:
    return Score.objects.filter(player_name=score.player_name, game_id__season_id=season).aggregate(models.Sum('score_impact')).get("score_impact__sum")