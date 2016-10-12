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
from google.appengine.ext import ndb

from models import User, RPS, Score
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm, ScoreForms
from models import GameForms

from utils import get_by_urlsafe


USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
    urlsafe_game_key=messages.StringField(1))
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(MakeMoveForm,
                                                urlsafe_game_key=messages.StringField(1),)
USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))
USER_GAME_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1))


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

    # Create a new user
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
        user_key = ndb.Key(User, request.email)
        print request.email
        print user_key
        user = User(key=user_key, name=request.user_name, email=request.email)
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
            user_key = user.key
            print user_key
            print user.email
            u_key = ndb.Key(User, user.email)
            print hash(u_key)
            game_id = RPS.allocate_ids(size=1, parent=u_key)[0]
            game_key = ndb.Key(RPS, game_id, parent=u_key)
            game = RPS.new_game(game_key, user.key, request.total_rounds)
            game.put()
        except:
            pass
        return game.to_form('Limber Up! Its rock paper scissor time!')

    # def _to_form(self, gaym):
    #     """Returns a GameForm """
    #     form = GameForm()
    #     for field in form.all_fields():
    #         print field, field.name
    #         if field.name == "message":
    #           print "test"
    #         elif field.name == "user_name":
    #           print "test"
    #         else:
    #           setattr(form, field.name, getattr(gaym, field.name))
    #     form.check_initialized()
    #     return form

    # Get the status of any game
    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, RPS)
        if game:
            if game.game_over:
                return game.to_form('Game is over. Stat a new game.')
            else:
                return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    def computer_move(self):
        """Returns a random choice from Rock-Paper-Scissors"""

        move_options = ['ROCK', 'PAPER', 'SCISSORS']
        return random.choice(move_options)

    # User makes a move (Actual gameplay)
    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='make_move',
                      name='make_move',
                      http_method='POST')
    def make_move(self, request):
        name = getattr(request, "user_name")
        user = User.query(User.name == name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')

        game = get_by_urlsafe(request.urlsafe_game_key, RPS)
        if game.game_over:
            return game.to_form('Game Over! Start a New Game')
        elif game.game_canceled:
            return game.to_form('Game was canceled. Choose another game to play.')
        else:
            rules = {"ROCK": "SCISSORS", "PAPER": "ROCK", "SCISSORS": "PAPER"}

            player = str(getattr(request, "play"))
            computer = self.computer_move()
            # print rules[player]
            if computer == player:
                message = "Its a tie!"
            elif rules[player] == computer:
                message = "Player wins this round!"
                game.player_points = game.player_points + 1
            else:
                message = "Computer wins this round!"
                game.computer_points = game.computer_points + 1

            game.rounds_remaining = game.rounds_remaining - 1
            if game.rounds_remaining == 0:
                game.end_game(game.player_points, game.computer_points)

            game.put()

            return game.to_form("Computer played %s. %s" % (computer, message))

    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])
        # return Hello(greeting="Hello World")

    @endpoints.method(request_message=USER_GAME_REQUEST,
                      response_message=GameForms,
                      path='games/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of a User's active games"""
        user = User.query(User.name == request.user_name).get()
        # print "test", user
        # print user.email
        gamez = RPS.query(ancestor=ndb.Key(User, user.email))
        return GameForms(items=[gaym.to_form("test") for gaym in gamez])

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      # response_message=Hello,
                      path='games/{urlsafe_game_key}/cancel',
                      name='cancel_games',
                      http_method='GET')
    def cancel_game(self, request):
        """Allows the user to cancel a game"""
        game = get_by_urlsafe(request.urlsafe_game_key, RPS)
        if game:
            if game.game_over:
                return game.to_form('Game is already over. Cannot cancel.')
            elif game.game_canceled:
                return game.to_form('Game already canceled.')
            else:
                game.game_canceled = True
                game.put()
                return game.to_form('Game canceled.')
        else:
            raise endpoints.NotFoundException('Game not found!')
        # return Hello(greeting="Hello World")

APPLICATION = endpoints.api_server([RPSApi])
