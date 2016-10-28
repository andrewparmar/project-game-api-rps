"""models.py - This file contains the class definitions for the Datastore
entities used by the game Rock-Paper-Scissors.
"""

from datetime import date
from protorpc import messages, message_types
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    # the following two items were added -> make changes below.
    total_points = ndb.IntegerProperty(default=0)
    total_rounds = ndb.IntegerProperty(default=0)
    win_rate = ndb.FloatProperty(default=0)

    def to_form(self):
        """Returns a GameForm representation of the Game"""
        return RankForm(name=self.name,
                        email=self.email,
                        total_points=self.total_points,
                        total_rounds=self.total_rounds,
                        win_rate=self.win_rate)


class RankForm(messages.Message):
    """GameForm for outbound game state information"""
    name = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)
    total_points = messages.IntegerField(3, required=True)
    total_rounds = messages.IntegerField(4, required=True)
    win_rate = messages.FloatField(5)


class RankForms(messages.Message):
    """RankForms -- multiple User rank outbound form message"""
    items = messages.MessageField(RankForm, 1, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)


class RPS(ndb.Model):
    """Game object"""
    rounds_total = ndb.IntegerProperty(required=True)
    rounds_remaining = ndb.IntegerProperty(required=True, default=5)
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    player_points = ndb.IntegerProperty(required=True, default=0)
    computer_points = ndb.IntegerProperty(required=True, default=0)
    game_canceled = ndb.BooleanProperty(default=False)
    move_log = ndb.StringProperty(repeated=True)

    @classmethod
    def new_game(cls, key, user, rounds):
        """Creates and returns a new rps game
        """
        game = RPS(key=key,
                   user=user,
                   rounds_total=rounds,
                   rounds_remaining=rounds,
                   game_over=False,
                   )
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
        form.player_points = self.player_points
        form.computer_points = self.computer_points
        form.game_canceled = self.game_canceled
        return form

    def end_game(self, player_points, computer_points):
        self.game_over = True
        score = 0
        game_won = False
        rounds = player_points + computer_points
        if player_points > computer_points:
            score = player_points - computer_points
            game_won = True
        # print "Players final score is:", score
        # print self.user.get().key
        new_score = Score(user=self.user.get().key, date=date.today(),
                          game_won=game_won, points=score, rounds=rounds)
        new_score.put()
        game_player = self.user.get()
        print "Poiints:", game_player.total_points
        game_player.total_points = game_player.total_points + player_points
        print "Rounds", game_player.total_rounds
        game_player.total_rounds = game_player.total_rounds + rounds

        game_player.win_rate = float(
            game_player.total_points) / game_player.total_rounds
        game_player.put()
        return "Jello World"

    def game_history(self):
        form = HistoryForm()
        form.user_name = self.user.get().name
        form.urlsafe_key = self.key.urlsafe()
        form.move_log = self.move_log
        return form


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    user_name = messages.StringField(2, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    rounds_remaining = messages.IntegerField(5, required=True)
    rounds_total = messages.IntegerField(6, required=True)
    player_points = messages.IntegerField(7, required=True)
    computer_points = messages.IntegerField(8, required=True)
    game_canceled = messages.BooleanField(9, required=True)


class GameForms(messages.Message):
    """GameForms -- multiple RPS outbound form message"""
    items = messages.MessageField(GameForm, 1, repeated=True)


class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)
    total_rounds = messages.IntegerField(5, default=5)


class MakeMoveForm(messages.Message):
    """Used to make a move in an existing game"""
    user_name = messages.StringField(1, required=True)
    play = messages.EnumField('MoveOptions', 2, required=True)


class HistoryForm(messages.Message):
    """Return the complete list of moves played in the game"""
    urlsafe_key = messages.StringField(1, required=True)
    user_name = messages.StringField(2, required=True)
    move_log = messages.StringField(3, repeated=True)


class MoveOptions(messages.Enum):
    """RPS - enumeration value"""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    game_won = ndb.BooleanProperty(required=True)
    points = ndb.IntegerProperty(required=True)
    rounds = ndb.IntegerProperty(required=True)

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name,
                         date=str(self.date),
                         game_won=self.game_won,
                         total_points=self.points,
                         total_rounds=self.rounds)


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    game_won = messages.BooleanField(3, required=True)
    total_points = messages.IntegerField(4, required=True)
    total_rounds = messages.IntegerField(5, required=True)


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)
