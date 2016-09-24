"""models.py - This file contains the class definitions for the Datastore
entities used by the game Rock-Paper-Scissors.
"""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)


class RPS(ndb.Model):
    """Game object"""
    rounds_total = ndb.IntegerProperty(required=True)
    rounds_remaining = ndb.IntegerProperty(required=True, default=5)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    # player_wins = ndb.IntegerProperty(required=True, default=0)
    # computer_wins = ndb.IntegerProperty(required=True, default=0)

    @classmethod
    def new_game(cls, user, rounds):
        """Creates and returns a new rps game
        """
        game = RPS(user=user,
                   rounds_total=rounds,
                   rounds_remaining=rounds,
                   game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.game_over = self.game_over
        form.rounds_total = self.rounds_total
        form.rounds_remaining = self.rounds_remaining
        form.message = message
        return form


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    user_name = messages.StringField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    rounds_remaining = messages.IntegerField(5, required=True)
    rounds_total = messages.IntegerField(6, required=True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    total_rounds = messages.IntegerField(5, default=5)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    user_name = messages.StringField(1, required=True)
    play = messages.EnumField('MoveOptions', 2, required=True)


class MoveOptions(messages.Enum):
    """RPS - enumeration value"""
    ROCK = 1
    PAPER = 2
    SCISSOR = 3


# class OutcomeForm(messages.Message):
#     """OutcomeForm for outbound round result information"""
#     urlsafe_key = messages.StringField(1, required=True)
#     user_name = messages.StringField(2, required=True)
#     message = messages.StringField(4, required=True)
