from app import db
from hashlib  import md5
from datetime import datetime

class User(db.Document):
    username   = db.StringField(required=True, unique=True)
    first_name = db.StringField(required=True)
    last_name  = db.StringField(required=True)
    email      = db.StringField(required=True, unique=True)
    password   = db.StringField(required=True)

    about_me   = db.StringField()
    last_seen  = db.DateTimeField(default=datetime.now)

    following  = db.ListField(db.ReferenceField('self'))

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            return self

    def is_following(self, user):
        return self.following.count(user) > 0

    def posts_from_following_users(self):
        users = [self] + self.following
        posts = Post.objects(author__in=users)
        return posts

    #required for flask-login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    #finish flask-login requirements

class Post(db.Document):
    author    = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    body      = db.StringField(required=True)
    timestamp = db.DateTimeField(default=datetime.now)

    meta = {
        'allow_inheritance': True,
        'ordering': ['-timestamp'],
        'indexes': [ #http://docs.mongoengine.org/guide/text-indexes.html
            {'fields': ['$body' ] }
        ],
    }

# class TextPost(Post):
    # body = StringField(required=True)

# class ImagePost(Post):
    # image_path = StringField()

# class LinkPost(Post):
    # link_url = StringField()

# class Comment(EmbeddedDocument):
    # content = StringField()
    # name    = StringField(max_length=120)
