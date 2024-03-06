from django import forms
from datetime import date
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError

class addPlayerForm(forms.Form):
    playerName = forms.CharField(label="Player")
    endPoints = forms.IntegerField(label="Points", step_size=100)

class addGameForm(forms.Form):
    gameDate = forms.DateField(label="Date", initial=date.today)
    gameNote = forms.CharField(label="Notes", max_length=1000, widget=forms.Textarea(attrs={"rows":"2"}), required=False)

class BasePlayerFormSet(BaseFormSet):
    season = None

    def clean(self):
        if any(self.errors):
            return
        
        players = []
        point_tally = 0
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                player = form.cleaned_data['playerName']
                points = form.cleaned_data['endPoints']

                if player:
                    if player in players:
                        form.add_error(field="playerName", error="Duplicate player.")
                        duplicates = True
                    players.append(player)
                
                point_tally += points

        if point_tally != (len(players) * self.season.season_starting_points):
            print((len(players) * self.season.season_starting_points))
            print(point_tally)
            for form in self.forms:
                form.add_error(field="endPoints", error="")
            raise forms.ValidationError(
                'Final points do not match starting points! %(missing_points)s Missing!',
                params={"missing_points": abs((len(players) * self.season.season_starting_points) - point_tally)},
                code='point_error'
            )