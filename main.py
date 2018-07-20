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



class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("main.html")
        self.response.write(template.render())







app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)






























































































###
