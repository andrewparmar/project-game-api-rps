#!/usr/bin/env python

"""
rps-api.py -- Udacity Game-API server-side Python App Engine API;
    uses Google Cloud Endpoints
"""

__author__ = 'andrew.parmar@gmail.com'

import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
from models import Hello

@endpoints.api(name='rock_paper_scissors', version='v1')
class RPSApi(remote.Service):
	"""Rock-Paper-Scissors API v1."""

    @endpoints.method(message_types.VoidMessage, Hello,
      path = "sayHello", http_method='GET', name = "sayHello")
    def say_hello(self, request):
      return Hello(greeting="Hello World")



APPLICATION = endpoints.api_server([RPSApi])