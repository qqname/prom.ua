from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64), unique=True, index=True)


    @property
    def password(self):
        raise AttributeError('Password is under protection')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))