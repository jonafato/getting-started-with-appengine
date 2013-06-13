from google.appengine.ext import db, blobstore

class User(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now_add=True)
    google_user = db.UserProperty(required=True)
    first_name = db.StringProperty(default='')
    last_name = db.StringProperty(default='')
    cat_photo = blobstore.BlobReferenceProperty()
    hobbies = db.StringListProperty()
    age = db.IntegerProperty(default=53)

    def display_name(self):
        if self.first_name or self.last_name:
           return self.first_name + ' ' + self.last_name
        return self.google_user.email()
