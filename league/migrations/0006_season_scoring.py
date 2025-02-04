# Generated by Django 5.0.3 on 2024-04-20 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0005_rename_player_name_player_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='scoring',
            field=models.TextField(choices=[('ADD', 'sum of all scores'), ('AVE', 'average performance'), ('TOP3', 'sum of best 3 scores'), ('TOP5', 'sum of best 5 scores'), ('STR3', 'best 3-game streak'), ('STR5', 'best 5-game streak')], default='ADD'),
        ),
    ]
