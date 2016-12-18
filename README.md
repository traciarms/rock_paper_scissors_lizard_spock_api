# Rock, Paper, Scissors, Lizard Spock Game API

## Description

User plays the game of Rock Paper Scissors Lizard Spock with the computer.

## Objectives

Offer enough endpoints to play the game:

### Endpoint:  '/games/'

* list of all games that have been played

### Endpoint: '/start/'

* Start a new game.
* Two inputs required: player's name and player move
* please note that double quotes are required around both the player's name
and the player's move
* also note that I didn't use curl commands to access the endpoints - I
used the browser.

### Endpoint: '/scores/'

* List of the top 10 player scores

### Endpoint: '/score/player_name/'

* Get the score for a particular player


## Curl Commands for accessing endpoints:

* curl http://127.0.0.1:8000/games/
* curl -X POST -H "Content-Type: application/json" -d
    '{
        "player": "Traci",
        "player_move": "SPOCK"
    }'
    http://127.0.0.1:8000/start/
* curl http://127.0.0.1:8000/scores/
* curl http://127.0.0.1:8000/score/Traci
* curl http://127.0.0.1:8000/computer_wins