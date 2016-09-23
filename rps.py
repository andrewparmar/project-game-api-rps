#!/usr/bin/env python

"""
rps-api.py -- Udacity Game-API server-side Python App Engine API;
    uses Google Cloud Endpoints
"""

# __author__ = 'andrew.parmar@gmail.com'

import random
import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote

from models import User, RPS
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm, OutcomeForm

from utils import get_by_urlsafe


USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1))
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(MakeMoveForm)


class Hello(messages.Message):
    """String that stores a message."""
    greeting = messages.StringField(1)


@endpoints.api(name='rock_paper_scissors', version='v1')
class RPSApi(remote.Service):
    """Rock-Paper-Scissors API v1."""

    @endpoints.method(message_types.VoidMessage,
                      Hello,
                      path='sayHello',
                      http_method='GET',
                      name='sayHello')
    def say_hello(self, unused_request):
        return Hello(greeting="Hello World")

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='create_user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(
                             request.user_name))

    # Create a new game.
    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      name='new_game',
                      path='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Create a new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        try:
            game = RPS.new_game(user.key, request.total_rounds)
        except:
            pass
        return game.to_form('Limber Up! Its rock paper scissor time!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, RPS)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=Hello,
                      path='make_move',
                      name='make_move',
                      http_method='POST')
    def make_move(self, request):
        name = getattr(request, "user_name")
        user = User.query(User.name == name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        name = getattr(request, "user_name")
        print name

        game = get_by_urlsafe(request.urlsafe_game_key, RPS)
        if game.game_over:
            return game.to_form('Game already over! Start a New Game')

        play = getattr(request, "play")
        print play
        print computer_move()

        return Hello(greeting="Hello World")
        # return OutcomeForm(user_name=name, message="Well Hello World")

    def computer_move(self):
        """Returns a random choice from Rock-Paper-Scissors"""

        move_options = ['Rock', 'Paper', 'Scissors']
        return random.choice(move_options)

APPLICATION = endpoints.api_server([RPSApi])
