"""models.py - This file contains the class definitions for the Datastore
entities used by the game Rock-Paper-Scissors.
"""

from datetime import date
from protorps import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()


class RPS(ndb.Model):
	"""Game object"""
	rounds_total = ndb.IntegerProperty(required=True)
    rounds_remaining = ndb.IntegerProperty(required=True, default=5)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')

    @classmethod
    def new_game(cls, user, rounds=3):
    	"""Creates and returns a new rps game
    	"""
    	game = RPS(user=user,
    			   rounds_total=rounds
    			   rounds_remaining=rounds,
    			   game_over=False)
    	game.put()
    	return game

    def end_game(self, won=False):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        # Add the game to the score 'board'
        # score = Score(user=self.user, date=date.today(), game_won=won,
        #               rounds_won = self.)
        # score.put()


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    rounds_remaining = messages.IntegerField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    user_name = messages.StringField(4, required=True)
    # message = messages.StringField(4, required=True)
 

class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    game_won = ndb.BooleanProperty(required=True)
    rounds_won = ndb.IntegerProperty(required=True)
    rounds_total = ndb.IntegerProperty(required=True)


class ScoreForm(message.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    game_won = messages.BooleanField(3, required=True)
    rounds_won = messages.IntegerField(4, required=True)
    rounds_total = messsages.IntegerProperty(5, required=True)


class MoveOptions(messages.Enum):
    """RPS - enumeration value"""
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

class Hello(messages.Message):
    """String that stores a message."""
    greeting = messages.StringField(1)