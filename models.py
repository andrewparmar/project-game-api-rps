"""models.py - This file contains the class definitions for the Datastore
entities used by the game Rock-Paper-Scissors.
"""

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
