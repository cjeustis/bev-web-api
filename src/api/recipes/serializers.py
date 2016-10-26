from flask_restplus import fields
from src.api.restplus import api

recipe = api.model('Recipe', {
  'id': fields.Integer(readOnly=True, description='The unique identifier of a recipe'),
  'name': fields.String(required=True, description='Name of a recipe'),
  'ingredients': fields.String(required=True, description='Ingredients for the recipe'),
  'imageUrl': fields.String(required=True, description='Image for the recipe')
})