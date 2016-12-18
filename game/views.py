import requests
from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Game, GAME_CHOICES
from game.serializers import GameSerializer, NewGameSerializer, ScoreSerializer, \
    ComputerComputerSerializer


class ListGameScores(generics.ListCreateAPIView):
    """
    A list view for the top 10 player scores.
    """
    model = Game
    queryset = Game.objects.filter(player_wins=True).values('player').order_by().\
        annotate(num_wins=Count('player_wins')).order_by('-num_wins')[:10]
    serializer_class = ScoreSerializer


class ComputerWins(APIView):
    """
    View total num of computer wins.
    """

    def get(self, request):
        """
        Return a count of all computer wins.
        """
        if request.method == 'GET':
            num_wins = len(Game.objects.filter(computer_wins=True).
                           annotate(num_wins=Sum('computer_wins')))
            return Response(num_wins)


class ScoreDetail(APIView):
    """
    View total wins for given player.
    """

    def get(self, request, player_name):
        """
        Return a count of all wins for this user.
        """
        if request.method == 'GET':
            if Game.objects.filter(player=player_name).exists():
                num_wins = len(Game.objects.
                               filter(player_wins=True, player=player_name).
                               annotate(num_wins=Count('player_wins'))
                               )
                return Response(num_wins)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)


class ListCreateGame(generics.ListCreateAPIView):
    """
    The view to create or play a new game
    """
    model = Game

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewGameSerializer
        return GameSerializer

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):

        player_move = request.data.get('player_move', 'rock')
        player_move = player_move.upper()

        # error checking from the user input
        choices = [ch[0] for ch in GAME_CHOICES]
        if player_move not in choices:
            return Response('PLEASE ENTER VALID INPUT: '
                            'ROCK, PAPER, SCISSORS, LIZARD, SPOCK',
                            status=status.HTTP_400_BAD_REQUEST)

        computer_move = self.get_computer_move(player_move)
        player_wins = self.get_player_wins(player_move, computer_move)
        computer_wins = self.get_computer_wins(player_wins)

        game = Game.objects.create(
            player=request.data.get('player', None),
            player_move=player_move,
            computer_move=computer_move,
            player_wins=player_wins,
            computer_wins=computer_wins
        )

        result = GameSerializer(game)
        return Response(result.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get_computer_move(player_move):
        """
        Get the computer move, I pass the player move to make sure there
        isn't a tie.
        :param player_move:
        :return:
        """
        player_move = player_move.upper()
        c_move = player_move

        while c_move == player_move:

            response = requests.get('http://codechallenge.boohma.com/random')
            number = response.json()
            r_num = number.get('random_number')

            if 1 < r_num <= 20:
                c_move = 'ROCK'
            elif 20 < r_num <= 40:
                c_move = 'PAPER'
            elif 40 < r_num <= 60:
                c_move = 'SCISSORS'
            elif 60 < r_num <= 80:
                c_move = 'LIZARD'
            elif 80 < r_num <= 100:
                c_move = 'SPOCK'

        return c_move

    @staticmethod
    def get_player_wins(player_move, computer_move):
        """
        Determine who wins given the player move and the computer move
        :param player_move:
        :param computer_move:
        :return:
        """
        player_wins = False
        player_move = player_move.upper()
        computer_move = computer_move.upper()

        if player_move == 'ROCK':
            if computer_move == 'SCISSORS' or computer_move == 'LIZARD':
                player_wins = True

        if player_move == 'PAPER':
            if computer_move == 'SPOCK' or computer_move == 'ROCK':
                player_wins = True

        if player_move == 'SCISSORS':
            if computer_move == 'LIZARD' or computer_move == 'PAPER':
                player_wins = True

        if player_move == 'LIZARD':
            if computer_move == 'SPOCK' or computer_move == 'PAPER':
                player_wins = True

        if player_move == 'SPOCK':
            if computer_move == 'SCISSORS' or computer_move == 'ROCK':
                player_wins = True

        return player_wins

    @staticmethod
    def get_computer_wins(player_wins):
        """
        The computer wins when the player didn't win
        :param player_wins:
        :return:
        """
        return not player_wins


class GameList(generics.ListAPIView):
    """
    List all the games.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
