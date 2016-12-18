# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-18 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(max_length=200)),
                ('player_wins', models.BooleanField(default=0)),
                ('player_move', models.CharField(choices=[(b'ROCK', b'rock'), (b'PAPER', b'paper'), (b'SCISSORS', b'scissors'), (b'LIZARD', b'lizard'), (b'SPOCK', b'spock')], default=b'rock', max_length=20)),
                ('computer_wins', models.BooleanField(default=0)),
                ('computer_move', models.CharField(choices=[(b'ROCK', b'rock'), (b'PAPER', b'paper'), (b'SCISSORS', b'scissors'), (b'LIZARD', b'lizard'), (b'SPOCK', b'spock')], default=b'rock', max_length=20)),
            ],
        ),
    ]
