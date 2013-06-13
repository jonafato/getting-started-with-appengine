from google.appengine.api import users
from models import User
import webapp2

class BaseHandler(webapp2.RequestHandler):
    @property
    def user(self):
        if not hasattr(self, '_user'):
            self._user = User.all().filter('google_user =', users.get_current_user()).get()
        return self._user
