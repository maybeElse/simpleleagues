# Generated by Django 5.0.3 on 2024-03-06 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0012_alter_rank_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='uma_3rd',
            field=models.IntegerField(default=-10),
        ),
        migrations.AddField(
            model_name='season',
            name='uma_4th',
            field=models.IntegerField(default=-20),
        ),
    ]
