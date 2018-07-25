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
    location = ndb.StringProperty(required=False)
    time = ndb.StringProperty(required=False)
    num = ndb.StringProperty(required=False)
    numGoing = ndb.StringProperty(required=False)
    attending = ndb.StringProperty(required=False, repeated=True)





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
        user.location = self.request.get("location")
        user.time = self.request.get("time")

        user.num = self.request.get("num")
        user.numGoing = "1"
        user.put()

        all_users = JUser.query()
        
        print (user.email)
        for otherUser in all_users:
            print (otherUser.attending)
            if user.email in otherUser.attending:
                print (user.email)
                otherUser.attending.remove(user.email)


        variables = {"user": user}
        template = jinja_environment.get_template("request.html")
        self.response.write(template.render(variables))


class MatchesHandler(webapp2.RequestHandler):
    def get(self):
        all_users = JUser.query()
        all_users = all_users.fetch(10)
        current_user = find_or_create_user()

        variables = {"all_users": all_users,
                     "current_user": current_user}
        template = jinja_environment.get_template("matches.html")
        self.response.write(template.render(variables))


    def post(self):
        all_users = JUser.query()
        all_users = all_users.fetch(10)
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

        mail.send_mail(sender=current_user.email, to=userEmail, subject="Meet2Eat", body=""" Your Meet2Eat request has been accepted by """ + current_user.name)

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("about.html")
        self.response.write(template.render())

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("calendar.html")
        self.response.write(template.render())



class PlacesHandler(webapp2.RequestHandler):
    def get(self):

        """request_headers = {"Accept-Language": "en-US,en;q=0.9",
                           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
                           "Accept": "application/json",
                           "Referer": "https://developers.zomato.com/",
                           "Connection": "keep-alive"
        }

        request = urllib2.Request("https://developers.zomato.com/", headers=request_headers)
        contents = urllib2.urlopen(request).read()
        print contents

        params = {
                  "q": "New York",
        }

        form_data = urllib.urlencode(params)
        api_url = "http://developers.zomato.com/api/v2.1/cities?"
        response = urllib2.urlopen(api_url + form_data)
        content = json.loads(response.read())
        city_id = content[0].id

        params = {
                  "city_id": content[0].id,
        }

        form_data = urllib.urlencode(results)
        api_url = "http://developers.zomato.com/api/v2.1/cuisines?"
        response = urllib2.urlopen(api_url + form_data)
        content = json.loads(response.read())
        cuisine_name = content[0].cuisine.cuisine_name

        template = jinja2_environment.get_template("places.html")
        variables = {"cuisine_name": cuisine_name}
        self.response.write(template.render(variables))"""
        template = jinja_environment.get_template("places.html")
        self.response.write(template.render())




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfileHandler),
    ('/about', AboutHandler),
    ('/request', RequestHandler),
    ('/matches', MatchesHandler),
    ('/calendar', CalendarHandler),
    ('/restaurants', PlacesHandler),
], debug=True)






























































































###
