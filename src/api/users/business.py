import logging
from flask import jsonify
from functools import wraps
from src.database import db
from src.database.models import User, Recipe, Ingredients
from itsdangerous import JSONWebSignatureSerializer
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
authUser = User("", "", "", False)

secret_key = "this_is_a_secret_0192837465)!@(*#$&^%)"
s = JSONWebSignatureSerializer(secret_key)
log = logging.getLogger(__name__)


def verify_token(f):
  @wraps(f)
  def verify_token(*args, **kwargs):
    global authUser
    token_state = authUser.verify_auth_token()
    if token_state is not "Valid":
      return {
        "message": "User cannot be authenticated: {} token".format(token_state)
      }
    return f(*args, **kwargs)
  return verify_token


def authenticate_user(data):
  global authUser
  _username = data.get('username')
  _password = data.get('password')

  user = User.query.filter(User.username == _username).first()
  if user is None:
    return {
      "message": "Error authenticating user. Username '{}' does not exist.".format(_username)
    }
  if not user.verify_password(_password):
    return {
      "message": "Error authenticating user. Password is invalid."
    }
  
  if user.username != authUser.username:
    token = user.generate_auth_token()
    authUser = user
  else:
    token = authUser.generate_auth_token()

  user.token = token
  return user


# Log out a User
def unauthenticate_user(user_id):
  global authUser
  if authUser.id is not "":
    authUser = User("", "", "")
  return None


# Create a new user
def create_user(data):
  global authUser
  _username = data.get('username')
  _email = data.get('email')
  _password = data.get('password')

  # Make sure username doesn't exist already
  exists = User.query.filter(User.username == _username).first()
  if exists is not None:
    return {
      "message": "Error creating user. Username '{}' already exists.".format(_username)
    }

  authUser = User(_username, _email, _password)
  db.session.add(authUser)
  db.session.commit()
  return authUser


# Try and find an existing user
def get_user(user_id):
  user = User.query.filter_by(id=user_id).first_or_404()
  return user


# Update an existing user
def update_user(user_id, data):
  user = User.query.filter_by(id=user_id).first()
  user.username = data.get('username')
  user.email = data.get('email')
  user.password = data.get('password')
  db.session.add(user)
  db.session.commit()
  return user


# Delete an existing user
def delete_user(user_id):
  user = User.query.filter(User.id == user_id).first_or_404()
  db.session.delete(user)
  db.session.commit()



# Try and find an existing recipe
def get_all_recipes(user_id):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first_or_404()
  
  if user:
    recipes = Recipe.query.join(Ingredients).filter(Recipe.user_id == user_id).all()
    return recipes

  return None


# Create a new recipe
def create_recipe(user_id, data):
  _name = data.get('name')
  _imageUrl = data.get('imageUrl')
  _ingredients = data.get('ingredients')

  # Should probably make sure the user_id exists...
  user = User.query.filter(User.id == user_id).first_or_404()
  if user:    
    recipe = Recipe(user_id, _name, _ingredients, _imageUrl)
    db.session.add(recipe)
    db.session.commit()
    return recipe

  return None

# Try and find an existing recipe
def get_recipe(user_id, recipe_id):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first_or_404()
  if user:
    recipe = Recipe.query.join(Ingredients).filter(Recipe.id == recipe_id).first_or_404()
    return recipe

  return None

# Update an existing recipe
def update_recipe(user_id, recipe_id, data):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first_or_404()
  if user:
    ourRecipe = Recipe.query.join(Ingredients).filter(Recipe.id == recipe_id).first_or_404()
    ings = []
    for ing in data.get('ingredients'):
      ings.append(Ingredients(ing.get('recipe_id'), ing.get('name')))
    ourRecipe.user_id = user_id
    ourRecipe.name = data.get('name')
    ourRecipe.ingredients = ings
    ourRecipe.imageUrl = data.get('imageUrl')
    db.session.add(ourRecipe)
    db.session.commit()
    return ourRecipe

  return None


# Delete an existingrecipeuser
def delete_recipe(user_id, recipe_id):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first_or_404()
  if user:
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first_or_404()
    db.session.delete(user)
    db.session.commit()