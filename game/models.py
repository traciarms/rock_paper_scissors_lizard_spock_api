
from django.db import models

GAME_CHOICES = (
    ('ROCK', 'rock'),
    ('PAPER', 'paper'),
    ('SCISSORS', 'scissors'),
    ('LIZARD', 'lizard'),
    ('SPOCK', 'spock')
)


class Game(models.Model):
    """Game object"""
    player = models.CharField(max_length=200)
    player_wins = models.BooleanField(default=0)
    player_move = models.CharField(max_length=20, choices=GAME_CHOICES, default="rock")
    computer_wins = models.BooleanField(default=0)
    computer_move = models.CharField(max_length=20, choices=GAME_CHOICES, default="rock")
