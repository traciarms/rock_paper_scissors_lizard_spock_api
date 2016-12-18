from rest_framework import serializers

from game.models import GAME_CHOICES


class ScoreSerializer(serializers.Serializer):
    """
    Score Serializer
    """
    player = serializers.CharField(max_length=200, read_only=True)
    num_wins = serializers.IntegerField(read_only=True)


class ComputerComputerSerializer(serializers.Serializer):
    """
    Computer Score Serializer
    """
    num_wins = serializers.IntegerField(read_only=True)


class NewGameSerializer(serializers.Serializer):
    """
    New Game Serializer
    """
    player = serializers.CharField(max_length=200)
    player_move = serializers.ChoiceField(choices=GAME_CHOICES,
                                          default='Rock')


class GameSerializer(serializers.Serializer):
    """
    Game Serializer
    """
    player = serializers.CharField(max_length=200)
    player_move = serializers.ChoiceField(choices=GAME_CHOICES,
                                          default='Rock')
    computer_move = serializers.ChoiceField(choices=GAME_CHOICES,
                                            read_only=True)
    player_wins = serializers.BooleanField(read_only=True)
    computer_wins = serializers.BooleanField(read_only=True)


