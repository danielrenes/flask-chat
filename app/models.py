from datetime import datetime, timedelta
from random import choice
from string import ascii_lowercase

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)

    messages = db.relationship('Message', backref='user')
    token = db.relationship('Token', uselist=False, backref='user')

    def generate_token(self):
        token = ''.join(choice(ascii_lowercase) for _ in range(128))
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        return {'token': token, 'expires_at': expires_at}

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
