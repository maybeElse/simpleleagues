from django.urls import path

from . import views

app_name = "league"
urlpatterns = [
    path("", views.index, name="index"),
    path("season/",views.index, name="season-index"),
    path("season/<slug:season_slug>",views.season, name="season"),
    # path("season/<slug:season_slug>/game/<int:game_id>", views.game, name="game"),
    # path("season/<slug:season_slug>/player/<str:player_name>", views.player, name="player"),
    path("player/<str:player_name>", views.player, name="player"),
    path("season/<slug:season_slug>/add", views.add_game, name="add_game")
]