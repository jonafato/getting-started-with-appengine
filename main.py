from base import BaseHandler
from datetime import datetime
from decorators import user_required
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp.blobstore_handlers import BlobstoreUploadHandler, BlobstoreDownloadHandler
from google.appengine.ext.webapp.util import login_required
from models import User
from webapp2_extras.routes import RedirectRoute

import jinja2
import logging
import os
import webapp2

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
    os.path.join(os.path.dirname(__file__), 'templates'))
)

class Home(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        self.response.out.write(template.render({}))

class Login(BaseHandler):
    @login_required
    def get(self):
        if not self.user:
            User(google_user=users.get_current_user()).put()
        self.redirect('/userinfo/')

class Logout(BaseHandler):
    def get(self):
        logout_url = users.create_logout_url('/')
        self.redirect(logout_url)

class Userinfo(BaseHandler):
    @user_required
    def get(self):
        User.all().filter('last_name =', 'fry')
        template = jinja_environment.get_template('userinfo.html')
        self.response.out.write(template.render({'user' : self.user, 'cat_photo_url' : blobstore.create_upload_url('/upload-cat-photo/')}))

class EditUserinfo(BaseHandler):
    @user_required
    def get(self):
        template = jinja_environment.get_template('userinfo-edit.html')
        self.response.out.write(template.render({'user' : self.user}))

    @user_required
    def post(self):
        self.user.first_name = self.request.get('first_name')
        self.user.last_name = self.request.get('last_name')
        if self.request.get('hobby'):
            self.user.hobbies.append(self.request.get('hobby'))
        self.user.put()
        self.redirect('/userinfo/')

class DownloadCatPhoto(BlobstoreDownloadHandler, BaseHandler):
    @user_required
    def get(self):
        if not self.user.cat_photo:
            self.error(404)
            return
        self.send_blob(self.user.cat_photo)

class UploadCatPhoto(BlobstoreUploadHandler, BaseHandler):
    @user_required
    def post(self):
        uploads = self.get_uploads('photo')
        if uploads:
            self.user.cat_photo = uploads[0]
            self.user.put()
        self.redirect('/userinfo/')

class CodeThatWontWork(BaseHandler):
    def get(self):
        # inequality issues
        User.all().filter('last_name !=', 'fry').filter('date_created <', datetime.now())
        User.all().filter('last_name !=', 'fry').order('-date_created')
        
        # things you'd expect to exist
        User.all().filter('last_name =', 'fry').exists()
        User.all().average('age')
        
        # i don't understand why this works this way
        User.all().fetch(limit=10, offset=1000000) # Takes forever.

app = webapp2.WSGIApplication([
    RedirectRoute('/', Home, name='home', strict_slash=True),
    RedirectRoute('/login/', Login, name='login', strict_slash=True),
    RedirectRoute('/logout/', Logout, name='logout', strict_slash=True),
    RedirectRoute('/userinfo/', Userinfo, name='userinfo', strict_slash=True),
    RedirectRoute('/userinfo/edit/', EditUserinfo, name='edit-userinfo', strict_slash=True),
    RedirectRoute('/upload-cat-photo/', UploadCatPhoto, name='upload-cat-photo', strict_slash=True),
    RedirectRoute('/download-cat-photo/', DownloadCatPhoto, name='download-cat-photo', strict_slash=True),
])
