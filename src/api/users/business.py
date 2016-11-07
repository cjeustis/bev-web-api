import logging
from flask import jsonify, abort, request
from functools import wraps
from src.database import db
from src.database.models import User, Recipe, Ingredients
from itsdangerous import JSONWebSignatureSerializer
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

secret_key = "this_is_a_secret_0192837465)!@(*#$&^%)"
s = JSONWebSignatureSerializer(secret_key)
log = logging.getLogger(__name__)


# Wrap endpoints with this to force the token of the user to be validated (it is located in the header)
def verify_token(f):
  @wraps(f)
  def verify_token(*args, **kwargs):
    token = request.headers.get('Auth-Token')
    if not token:
      return {
        "message": "User is not authenticated."
      }
    # First query the database to see if the token exists to someone
    # If it doesn't it means it is invalid
    user = User.query.filter_by(token=token).first()
    if user is None:
      return {
        "message": "User is not authenticated."
      }
      
    if User.verify_auth_token(token) is not "Valid":
      return {
        "message": "User is not authenticated: {} token".format(token_state)
      }
    return f(*args, **kwargs)
  return verify_token


def authenticate_user(data):
  _username = data.get('username')
  _password = data.get('password')

  user = User.query.filter(User.username == _username).first()
  if user is None:
    abort(400, "Error authenticating user. Username '{}' does not exist.".format(_username))
  if not user.verify_password(_password):
    abort(400, "Error authenticating user. Password is invalid.")
  
  # Get token for the user
  user.generate_auth_token()
  db.session.add(user)
  db.session.commit()
  return {
    'token': user.token,
    'user': user
  }


# Log out a User
def unauthenticate_user(user_id):
  # Make sure username doesn't exist already
  user = User.query.filter_by(id=user_id).first()
  if user is None:
    abort(400, "Could not log out user. User {} does not exist.".format(user_id))

  # If they don't have a token, do nothing
  if user.token is None:
    return None
  
  user.token = None
  db.session.add(user)
  db.session.commit()
  return None


# Create a new user
def create_user(data):
  _username = data.get('username')
  _email = data.get('email')
  _password = data.get('password')

  # Make sure username doesn't exist already
  user = User.query.filter(User.username == _username).first()
  if user is not None:
    abort(400, "Error creating user. Username '{}' already exists.".format(_username))

  newUser = User(_username, _email, _password)
  log.info("newUser: {}".format(newUser))
  db.session.add(newUser)
  db.session.commit()
  return {
    'token': newUser.token,
    'user': newUser
  }


# Try and find an existing user
def get_user(user_id):
  user = User.query.filter_by(id=user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))
  return user


# Update an existing user
def update_user(user_id, data):
  user = User.query.filter_by(id=user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))
  user.username = data.get('username')
  user.email = data.get('email')
  user.password = data.get('password')
  db.session.add(user)
  db.session.commit()
  return user


# Delete an existing user
def delete_user(user_id):
  user = User.query.filter(User.id == user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))
  db.session.delete(user)
  db.session.commit()



# Try and find an existing recipe
def get_all_recipes(user_id):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))
  
  recipes = Recipe.query.join(Ingredients).filter(Recipe.user_id == user_id).all()
  return recipes


# Create a new recipe
def create_recipe(user_id, data):
  _name = data.get('name')
  _imageUrl = data.get('imageUrl')
  _ingredients = data.get('ingredients')

  # Should probably make sure the user_id exists...
  user = User.query.filter(User.id == user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))

  recipe = Recipe(user_id, _name, _ingredients, _imageUrl)
  db.session.add(recipe)
  db.session.commit()
  return recipe


# Try and find an existing recipe
def get_recipe(user_id, recipe_id):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))

  recipe = Recipe.query.join(Ingredients).filter(Recipe.id == recipe_id).first()
  if recipe is None:
    abort(404, "Could not find a recipe for user ({}) with id: {}".format(user_id, recipe_id))
  return recipe


# Update an existing recipe
def update_recipe(user_id, recipe_id, data):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))

  ourRecipe = Recipe.query.join(Ingredients).filter(Recipe.id == recipe_id).first()
  if recipe is None:
    abort(404, "Could not find a recipe for user ({}) with id: {}".format(user_id, recipe_id))

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


# Delete an existingrecipeuser
def delete_recipe(user_id, recipe_id):
  # Make sure user exists
  user = User.query.filter(User.id == user_id).first()
  if user is None:
    abort(404, "Could not find a user with id: {}".format(user_id))
  recipe = Recipe.query.filter(Recipe.id == recipe_id).first_or_404()
  db.session.delete(user)
  db.session.commit()