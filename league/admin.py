from django.contrib import admin

# Register your models here.

from .models import *

class SeasonAdmin(admin.ModelAdmin):
    list_display = ("season_name", "season_notes", "season_active")
    prepopulated_fields = {"season_slug": ["season_name"]}

admin.site.register(Season, SeasonAdmin)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Rank)