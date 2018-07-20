import os
import jinja2
import webapp2
import json
import urllib
import urllib2
from google.appengine.ext import ndb



jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(
        os.path.dirname(__file__) + '/templates'))



class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("main.html")
        self.response.write(template.render())







app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)






























































































###
