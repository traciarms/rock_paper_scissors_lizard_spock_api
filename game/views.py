import requests
from django.db.models import Count, Sum
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from game.models import Game, GAME_CHOICES
from game.serializers import GameSerializer, NewGameSerializer, ScoreSerializer


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
        if not game:
            return Response('Item couldn\'t be created with input',
                            status=status.HTTP_400_BAD_REQUEST)

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
        mod_lookup = {
            0: 'ROCK',
            1: 'PAPER',
            2: 'SCISSORS',
            3: 'LIZARD',
            4: 'SPOCK'
        }

        while c_move == player_move:

            response = requests.get('http://codechallenge.boohma.com/random')
            number = response.json()
            r_num = number.get('random_number')
            mod = r_num % 5
            c_move = mod_lookup[mod]

        return c_move

    @staticmethod
    def get_player_wins(player_move, computer_move):
        """
        Determine who wins given the player move and the computer move
        :param player_move:
        :param computer_move:
        :return:
        """
        player_move = player_move.upper()
        computer_move = computer_move.upper()
        player_win_lookups = {
            'ROCK': ['SCISSORS', 'LIZARD'],
            'PAPER': ['SPOCK', 'ROCK'],
            'SCISSORS': ['LIZARD', 'PAPER'],
            'LIZARD': ['SPOCK', 'PAPER'],
            'SPOCK': ['SCISSORS', 'ROCK']
        }

        return computer_move in player_win_lookups[player_move]


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
