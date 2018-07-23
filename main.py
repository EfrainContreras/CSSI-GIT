import os
import jinja2
import webapp2
import json
import urllib
import urllib2
from google.appengine.ext import ndb
from google.appengine.api import users


jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))

# TO-DO:
# 1. Add a way to login and keep track of diffrent users
# 2. Request input from users
# 3. Make a grid displaying all request mades with info of the user who requested
# 4. A way to block people who abuse the app
# 5. Messaging between users



# START STORE USER INFO
class JUser(ndb.Model):
    nickname =  ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)




class MainPage(webapp2.RequestHandler):
    def get(self):

        user = 0
        log_url = False

        variables = {"user": user,
                    "log_url": log_url}


        template = jinja_environment.get_template("main.html")
        self.response.write(template.render(variables))

class ProfileHandler(webapp2.RequestHandler):
        template = jinja_environment.get_template("profile.html")

class AboutHandler(webapp2.RequestHandler):
        template = jinja_environment.get_template("about.html")

class ProfileHandler(webapp2.RequestHandler):
    def get(self):


        template = jinja_environment.get_template("profile.html")
        self.response.write(template.render())




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfileHandler),
    ('/about',AboutHandler),
], debug=True)






























































































###
