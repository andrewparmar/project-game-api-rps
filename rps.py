#!/usr/bin/env python

"""
rps-api.py -- Udacity Game-API server-side Python App Engine API;
    uses Google Cloud Endpoints
"""

# __author__ = 'andrew.parmar@gmail.com'

import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote

from models import User
from models import StringMessage


USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))


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
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email)
        user.put()
        return StringMessage(message='User {} created!'.format(request.user_name))


APPLICATION = endpoints.api_server([RPSApi])
