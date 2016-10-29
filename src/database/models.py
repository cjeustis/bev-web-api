# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from src.database import db
from api.restplus import api


#User Model
class User(db.Model):
  id = db.Column('user_id', db.Integer, primary_key=True)
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
    self.id = 0


# Recipe Model
class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  ingredients = db.Column(db.String(80))
  imageUrl = db.Column(db.String(80))
  created = db.Column(db.DateTime)

  def __init__(self, name, ingredients, imageUrl, created=None):
    self.name = name
    self.ingredients = ingredients
    if created is None:
      created  = datetime.utcnow()
    self.created = created
    self.imageUrl = imageUrl