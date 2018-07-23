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


# START LOGIN INFO
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
# END LOGIN INFO



# START STORE USER INFO
class JUser(ndb.Model):
    nickname =  ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)




class MainPage(webapp2.RequestHandler):
    def get(self):

        user = find_or_create_user()
        log_url = get_log_inout_url(user)

        variables = {"user": user,
                    "log_url": log_url}


        template = jinja_environment.get_template("main.html")
        self.response.write(template.render(variables))





app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)






























































































###
