from flask_restplus import fields
from src.api.restplus import api

user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

ingredients = api.model('Ingredients', {
  # 'id': fields.Integer(readOnly=True, description='The unique identifier of an ingredient'),
  # 'recipe_id': fields.Integer(readOnly=True, description='The recipe the ingredient belongs to'),
  'name': fields.String(required=True, description='Name of the ingredient'),
})

recipe = api.model('Recipe', {
  # 'id': fields.Integer(readOnly=True, description='The unique identifier of a recipe'),
  # 'user_id': fields.Integer(readOnly=True, description='The user the recipe belongs to'),
  'name': fields.String(required=True, description='Name of a recipe'),
  'ingredients': fields.List(fields.Nested(ingredients)),
  'imageUrl': fields.String(required=True, description='Image for the recipe')
})