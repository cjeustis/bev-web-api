# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from datetime import datetime
from src.database import db
from api.restplus import api
import logging

log = logging.getLogger(__name__)


# Ingredients Model
class Ingredients(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
  name = db.Column(db.String(200))

  def __init__(self, recipe_id, name):
    self.recipe_id = recipe_id
    self.name = name


# Recipe Model
class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  name = db.Column(db.String(80))
  ingredients = db.relationship('Ingredients', backref='recipe', lazy='dynamic')
  imageUrl = db.Column(db.String(80))
  created = db.Column(db.DateTime)

  def __init__(self, user_id, name, ingredients, imageUrl, created=None):
    self.user_id = user_id
    self.name = name
    self.ingredients = []
    for ing in ingredients:
      if 'name' in name:
        name = ing.name
      if name is None:
        name = ing.get('name')
      self.ingredients.append(Ingredients(self.id, name))

    if created is None:
      created  = datetime.utcnow()
    self.created = created
    self.imageUrl = imageUrl

  def __repr__(self):
    return '<Recipe: user_id: %s, name: %s, imageUrl: %s>' % (self.user_id, self.name, self.imageUrl)


#User Model
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80))
  email = db.Column(db.String(80))
  password = db.Column(db.String(80))
  created = db.Column(db.DateTime)
  recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

  def __init__(self, username, email, password, recipes=[], created=None):
    self.username = username
    self.email = email
    self.password = password      
    self.recipes = recipes
    if created is None:
      created  = datetime.utcnow()
    self.created = created