from __future__ import print_function
import os
import jinja2
import webapp2
import json
import urllib
import urllib2
import base64
import mimetypes
import smtplib
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient.discovery import build
from google.appengine.ext import vendor
from google.appengine.api import mail
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors


vendor.add('lib')


jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))

# TO-DO:
# 1. Add a way to login and keep track of diffrent users
# 2. Request input from users
# 3. Make a grid displaying all request mades with info of the user who requested
# 4. A way to block people who abuse the app
# 5. Messaging between users
def find_or_create_user():
     user = users.get_current_user()
     if user:
         key = ndb.Key('JUser', user.user_id())
         juser = key.get()
         if not juser:
             juser = JUser(key=key,
                           nickname=user.nickname(),
                           email=user.email()
                           )
         juser.put()
         return juser;
     return None

def get_log_inout_url(user):
     if user:
         return users.create_logout_url('/')
     else:
         return users.create_login_url('/')


# START STORE USER INFO
class JUser(ndb.Model):
    nickname =  ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    bio = ndb.StringProperty(required=False)
    name = ndb.StringProperty(required=False)
    phone = ndb.StringProperty(required=False)
    time = ndb.StringProperty(required=False)
    date = ndb.StringProperty(required=False)
    num = ndb.StringProperty(required=False)
    numGoing = ndb.StringProperty(required=False)
    attending = ndb.StringProperty(required=False, repeated=True)
    genderPref = ndb.StringProperty(required=False)
    gender = ndb.StringProperty(required=False)
    city = ndb.StringProperty(required=False)
    state = ndb.StringProperty(required=False)
    address = ndb.StringProperty(required=False)
    uCity = ndb.StringProperty(required=False)
    uState = ndb.StringProperty(required=False)







class MainPage(webapp2.RequestHandler):
    def get(self):

        user = find_or_create_user()
        log_url = get_log_inout_url(user)



        variables = {"user": user,
                    "log_url": log_url}
        template = jinja_environment.get_template("main.html")
        self.response.write(template.render(variables))


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = find_or_create_user()
        variables = {"user": user}
        template = jinja_environment.get_template("profile.html")
        self.response.write(template.render(variables))


    def post(self):
        user = find_or_create_user()
        user.name = self.request.get("name")
        user.bio = self.request.get("bio")
        user.phone = self.request.get("phone")
        user.gender = self.request.get("gender")
        user.uCity = self.request.get("uCity")
        user.uState = self.request.get("uState")
        user.put()

        variables = {"user": user}
        template = jinja_environment.get_template("profile.html")
        self.response.write(template.render(variables))


class RequestHandler(webapp2.RequestHandler):
    def get(self):
        user = find_or_create_user()

        variables = {"user": user}
        template = jinja_environment.get_template("request.html")
        self.response.write(template.render(variables))

    def post(self):
        user = find_or_create_user()
        user.date = self.request.get('date')
        user.time =  self.request.get('time')
        user.num = self.request.get("num")
        user.genderPref = self.request.get("genderPref")
        user.numGoing = "1"
        user.city = self.request.get("city")
        user.state = self.request.get("state")
        user.address = self.request.get("address")

        user.put()

        all_users = JUser.query()
        for otherUser in all_users:
            print (otherUser.attending)
            if user.email in otherUser.attending:
                otherUser.attending.remove(user.email)
                otherUser.put()


        current_date = str(datetime.datetime.today()).split()[0]


        variables = {"user": user,
                     "current_date": current_date}
        template = jinja_environment.get_template("request.html")
        self.response.write(template.render(variables))


class MatchesHandler(webapp2.RequestHandler):
    def get(self):
        all_users = JUser.query()
        all_users = all_users.fetch()
        current_user = find_or_create_user()

        variables = {"all_users": all_users,
                     "current_user": current_user}

        template = jinja_environment.get_template("matches.html")
        self.response.write(template.render(variables))


    def post(self):
        all_users = JUser.query()
        all_users = all_users.fetch()
        current_user = find_or_create_user()

        userEmail = self.request.get("user.email")
        user_query = JUser.query().filter(JUser.email == userEmail).fetch(1)[0]

        if not(userEmail in current_user.attending):
            current_user.attending.append(userEmail)
            current_user.put()

        user_query.num = str(int(user_query.num) - 1)
        user_query.numGoing = str(int(user_query.numGoing) + 1)

        user_query.put()

        variables = {"all_users": all_users,
                     "current_user": current_user}
        template = jinja_environment.get_template("matches.html")
        self.response.write(template.render(variables))

        mail.send_mail(sender="meet2eatdining@gmail.com", to=userEmail, subject="Meet2Eat", body=current_user.name + " has accepted your Meet2Eat request to eat at " + user_query.address + " at " + user_query.time + " on " + {{user_query.date}})


class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        all_users = JUser.query()
        all_users = all_users.fetch()
        current_user = find_or_create_user()

        current_date = str(datetime.datetime.today()).split()[0]

        variables = {"all_users": all_users,
                     "current_user": current_user,
                     "current_date": current_date}
        template = jinja_environment.get_template("calendar.html")
        self.response.write(template.render(variables))


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("about.html")
        self.response.write(template.render())

class PlacesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("places.html")
        self.response.write(template.render())

class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("success.html")
        self.response.write(template.render())

    def post(self):
        current_user = find_or_create_user()
        current_user.city = self.request.get("city")
        current_user.state = self.request.get("state")
        current_user.state = self.request.get("address")

        current_user.put()

        template = jinja_environment.get_template("success.html")
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfileHandler),
    ('/about', AboutHandler),
    ('/request', RequestHandler),
    ('/matches', MatchesHandler),
    ('/calendar', CalendarHandler),
    ('/places', PlacesHandler)
], debug=True)






























































































### This code is great don't @ me
