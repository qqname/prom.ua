from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager
import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64), unique=True, index=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=True)


    @property
    def password(self):
        raise AttributeError('Password is under protection')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Channel(db.Model):
    __tablename__='channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    descr = db.Column(db.String(1000), index=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    users = db.relationship('User', backref='channel')

    def __repr__(self):
        return '<Channel: %r>' % self.name