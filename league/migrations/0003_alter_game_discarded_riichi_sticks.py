# Generated by Django 5.0.3 on 2024-03-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0002_game_discarded_riichi_sticks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='discarded_riichi_sticks',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
