# Generated by Django 5.0.3 on 2024-03-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='season_slug',
            field=models.SlugField(default=models.CharField(max_length=32, unique=True), unique=True),
        ),
    ]
