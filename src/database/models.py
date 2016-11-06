from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from src.database import db
from api.restplus import api
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import logging

log = logging.getLogger(__name__)
secret_key = "this_is_a_secret_0192837465)!@(*#$&^%)"


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
  password = db.Column(db.String(200))
  created = db.Column(db.DateTime)
  recipes = db.relationship('Recipe', backref='user', lazy='dynamic')
  _token = ""

  def hash_password(self, password):
    self.password = pwd_context.encrypt(password)
  
  def verify_password(self, password):
    return pwd_context.verify(password, self.password)

  def generate_auth_token(self, expiration = 20):
    # Check if valid token already exists, otherwise we can generate a new one
    token_state = self.verify_auth_token()
    if token_state is "Valid":
      return self._token
    s = Serializer(secret_key, expires_in = expiration)
    self._token = s.dumps({ 'id': self.id })
    return self._token

  def verify_auth_token(self):
    s = Serializer(secret_key)
    try:
      data = s.loads(self._token)
    except SignatureExpired:
      return "Expired"
    except BadSignature:
      return "Invalid"
    return "Valid"

  def __init__(self, username, email, password, createToken=True, recipes=[], created=None):
    self.username = username
    self.email = email
    self.password = pwd_context.encrypt(password)
    self.recipes = recipes
    if created is None:
      created  = datetime.utcnow()
    self.created = created
    if createToken:
      self._token = self.generate_auth_token()