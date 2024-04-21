from .models import *
from django.db import models
from django.core import exceptions
from collections import Counter

def calculate_and_save_scores(game: Game, season: Season, scores: list, uma_spread: list):
    '''
    Placement order logic

    First, make sure the array is sorted; then, figure out which place each player is in.
    Account for ties if necessary.
    '''
    scores = sorted(scores, key=lambda d: d['score'], reverse=True)

    for i, scoreAndPlayer, tied in score_loop_helper(scores):
        place = i+1
        if not (tied is 1 or i is 0):
            for x in range(1, tied):
                if scores[i-x].get("score") > scoreAndPlayer.get("score"):
                    break
                place = i+1-x

        uma = sum(uma_spread[place-1:][:tied])/tied
        
        '''
        Calculate the individual score and store all of that information in the database
        '''
        score = Score.objects.create(
            player_name = scoreAndPlayer.get("player"),
            game_id = game,
            score_final = scoreAndPlayer.get("score"),
            score_position = Score.ScorePositions(place),
            score_penalty = scoreAndPlayer.get("penalty"),
            score_uma = uma,
            score_impact = 
                (scoreAndPlayer.get("score") - season.starting_points)/1000
                + season.oka + uma - scoreAndPlayer.get("penalty")
        )

        '''
        Calculate overall league performance, using whichever score calculation method the season is set to use
        '''
        rank, created = Rank.objects.update_or_create(
            player_name = scoreAndPlayer.get("player"),
            season_id = season,
            defaults = {
                "score": calculate_rank(score, season)
            }
        )

'''
This is just to make the for loop in calculate_scores() a bit prettier.
'''
def score_loop_helper(scores):
    r = []
    scoreCount = Counter(item.get("score") for item in scores)
    for i in range(len(scores)):
        r.append(
            (i, scores[i], scoreCount.get(scores[i].get("score"))
            )
        )
    return r

def calculate_rank(score: Score, season: Season):
    scoring = Season.ScoringTypes(season.scoring)
    scores = Score.objects.filter(player_name=score.player_name, game_id__season_id=season)

    match scoring:
        case Season.ScoringTypes.cumulative:
            return scores.aggregate(models.Sum('score_impact')).get("score_impact__sum")
        case Season.ScoringTypes.average:
            return scores.aggregate(models.Sum('score_impact')).get("score_impact__sum")/scores.count()
        case Season.ScoringTypes.best_3:
            return best_games(score, season, 3)
        case Season.ScoringTypes.best_5:
            return best_games(score, season, 5)
        case Season.ScoringTypes.best_streak_3:
            return best_streak(score, season, 3)
        case Season.ScoringTypes.best_streak_5:
            return best_streak(score, season, 5)
        case _:
            raise exceptions.ImproperlyConfigured("Season scoring is misconfigured!")
    
def best_streak(scores, count: int):
    if scores.count() < count:
        return 0
    scores.order_by('game_id__game_number_in_season')

    # TK need to implement
    return 0

def best_games(scores, count: int):
    if scores.count() < count:
        return 0
    return scores.order_by('-score_impact')[:count].aggregate(models.Sum('score_impact')).get("score_impact__sum")