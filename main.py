#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from rps import RPSApi

from models import User, RPS


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games that are incomplete.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        games = RPS.query(RPS.game_over == False)
        for game in games:
            key_id = game.user.string_id()
            print key_id
            users = User.query(User.email == key_id)
            for user in users:
                print user.name
        # users = User.query(User.email != None)
        # for user in users:
                subject = 'You have unfinished RPS business!'
                body = 'Hello {}, settle your RPS duel - make a new move!\n Your came id is {}'.format(user.name,game.)
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
], debug=True)
