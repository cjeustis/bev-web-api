# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from src.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    created = db.Column(db.DateTime)

    def __init__(self, username, email, password, created=None):
        self.username = username
        self.email = email
        if created is None:
            created  = datetime.utcnow()
        self.created = created
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username