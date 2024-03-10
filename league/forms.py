from django import forms
from datetime import date
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError

class addPlayerForm(forms.Form):
    playerName = forms.CharField(label="Player",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Player'}
                                ))
    endPoints = forms.IntegerField(label="Points", step_size=100,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Final score'}
                                ))
    penalty = forms.IntegerField(label="Penalty (only if points discarded)", required=False,
                                max_value=100, min_value=0, initial=0,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Penalty (if any)'}
                                ))


class addGameForm(forms.Form):
    gameDate = forms.DateField(label="Date", initial=date.today,
                               widget=forms.NumberInput(
                                   attrs={'type': 'date'}
                               ))
    gameNote = forms.CharField(label="Notes", max_length=1000, widget=forms.Textarea(attrs={"rows":"2"}), required=False)
    gameDiscardedRiichi = forms.IntegerField(label="Lost sticks", step_size=1000, required=False,
                                min_value=0,
                                widget = forms.NumberInput(
                                    attrs={'placeholder': 'Riichi sticks left on table (if any)'}
                                ))

class BasePlayerFormSet(BaseFormSet):
    season = None

    def __init__(self, *args, **kwargs):
        try:
            self.gameForm = kwargs.pop('gameForm')
        except KeyError:
            pass
        super(BasePlayerFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        if any(self.errors):
            return
        
        players = []
        point_tally = 0
        try:
            point_tally += self.gameForm.cleaned_data['gameDiscardedRiichi']
        except TypeError:
            pass

        for form in self.forms:
            if form.cleaned_data:
                player = form.cleaned_data['playerName']
                points = form.cleaned_data['endPoints']

                if player:
                    if player in players:
                        form.add_error(field="playerName", error="Duplicate player.")
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