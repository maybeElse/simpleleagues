from django.db import models
from django.urls import reverse
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from functools import total_ordering

class Season(models.Model):
    season_name = models.CharField(max_length=32, unique=True)
    season_notes = models.TextField(blank=True)
    class GameTypes(models.IntegerChoices):
        sanma = 3, _("Sanma (3-player)")
        riichi = 4, _("Riichi Mahjong (4-player)")
    season_type = models.IntegerField(choices=GameTypes, default=GameTypes.riichi)
    active = models.BooleanField(default=True)

    starting_points = models.IntegerField(choices=[(25000,"25,000"),(30000,"30,000"),(35000,"35,000")], default=30000)

    oka = models.IntegerField(default=0)   
    uma_big = models.IntegerField(default=20)
    uma_small = models.IntegerField(default=10)

    slug = models.SlugField(unique=True, null=False)
    def get_absolute_url(self):
        return reverse("season", kwargs={"slug": self.slug})

@total_ordering
class Player(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    def __eq__(self, other):
        # if not self._is_valid_operand(other):
        #     return NotImplemented
        return ((self.name.lower(), self.name.lower()) ==
                (other.name.lower(), other.name.lower()))
    def __lt__(self, other):
        # if not self._is_valid_operand(other):
        #     return NotImplemented
        return ((self.name.lower(), self.name.lower()) <
                (other.name.lower(), other.name.lower()))

class Game(models.Model):
    season_id = models.ForeignKey(Season, on_delete=models.PROTECT)
    game_notes = models.TextField(blank=True)
    game_date = models.DateField(default=date.today)
    game_number_in_season = models.IntegerField(default=1)
    discarded_riichi_sticks = models.IntegerField(default=0, null=True)

class Score(models.Model):
    player_name = models.ForeignKey(Player, on_delete=models.PROTECT)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    score_penalty = models.IntegerField(default=0)
    score_final = models.IntegerField()
    
    class ScorePositions(models.IntegerChoices):
        first = 1, "1st"
        second = 2, "2nd"
        third = 3, "3rd"
        fourth = 4, "4th"
        fifth = 5, "5th"
    score_position = models.IntegerField(choices=ScorePositions)

    score_uma = models.IntegerField()
    score_impact = models.FloatField()

class Rank(models.Model):
    player_name = models.ForeignKey(Player, on_delete=models.PROTECT)
    season_id = models.ForeignKey(Season, on_delete=models.CASCADE)
    score = models.FloatField(default=0)