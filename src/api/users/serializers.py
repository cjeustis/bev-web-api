from flask_restplus import fields
from src.api.restplus import api

ingredients = api.model('Ingredients', {
  'id': fields.Integer(readOnly=True, description='The unique identifier of a ingredient'),
  'name': fields.String(required=True, description='Name of the ingredient'),
})

recipe = api.model('Recipe', {
  'id': fields.Integer(readOnly=True, description='The unique identifier of a recipe'),
  'user_id': fields.Integer(readOnly=True, description='The user the recipe belongs to'),
  'name': fields.String(required=True, description='Name of a recipe'),
  'ingredients': fields.List(fields.Nested(ingredients)),
  'imageUrl': fields.String(required=True, description='Image for the recipe')
})

user = api.model('User', {
  'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
  'username': fields.String(required=True, description='Username of the user'),
  'email': fields.String(required=True, description='Email of the user'),
  'password': fields.String(required=True, description='Password of the user'),
  'recipes': fields.List(fields.Nested(recipe))
})

user_info = api.model('UserInfo', {
  'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
  'username': fields.String(required=True, description='Username of the user'),
  'email': fields.String(required=True, description='Email of the user'),
  'recipes': fields.List(fields.Nested(recipe))
})

user_login = api.model('UserLogin', {
  'username': fields.String(required=True, description='Username of the user'),
  'password': fields.String(required=True, description='Password of the user')
})

user_auth = api.model('UserAuth', {
  'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
  'username': fields.String(required=True, description='Username of the user'),
  'email': fields.String(required=True, description='Email of the user'),
  'recipes': fields.List(fields.Nested(recipe)),
  'token': fields.String(required=True, description='Security token for authorization')
})

user_registration = api.model('UserRegistration', {
  # 'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
  'username': fields.String(required=True, description='Username of the user'),
  'email': fields.String(required=True, description='Email of the user'),
  'password': fields.String(required=True, description='Password of the user')
})

token_response = api.model('TokenResponse', {
  'token': fields.String(required=True, description='Security token for authorization'),
  'user': fields.Nested(user_info)
})