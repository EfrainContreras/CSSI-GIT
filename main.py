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
        user.put()

        variables = {"user": user}
        template = jinja_environment.get_template("request.html")
        self.response.write(template.render(variables))

class MatchesHandler(webapp2.RequestHandler):
    def get(self):
        all_users = JUser.query()

        all_users = all_users.fetch(10)
        print (all_users)

        current_user = find_or_create_user()

        variables = {"all_users": all_users,
                     "current_user": current_user}
        template = jinja_environment.get_template("matches.html")
        self.response.write(template.render(variables))

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
        params = {"user-key": "5e5eb7cd8cd86731avb324d76be57bc17",
                  "q": "New York",
        }

        form_data = urllib.urlencode(params)
        api_url = "http://developers.zomato.com/api/v2.1/cities?"
        response = urllib2.urlopen(api_url + form_data)
        content = json.loads(response.read())
        city_id = content[0].id

        params = {"user-key": "e5eb7cd8cd86731avb324d76be57bc17",
                  "city_id": content[0].id,
        }

        form_data = urllib.urlencode(params)
        api_url = "http://developers.zomato.com/api/v2.1/cuisines?"
        response = urllib2.urlopen(api_url + form_data)
        content = json.loads(response.read())
        cuisine_name = content[0].cuisine.cuisine_name

        template = jinja2_environment.get_template("places.html")
        variables = {"cuisine_name": cuisine_name}
        self.response.write(template.render(variables))





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
