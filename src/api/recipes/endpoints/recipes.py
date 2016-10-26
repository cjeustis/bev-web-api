import logging
from flask import request
from flask_restplus import Resource
from src.api.recipes.business import create_recipe, delete_recipe, update_recipe
from src.api.recipes.serializers import recipe
from src.api.restplus import api
from src.database.models import Recipe

log = logging.getLogger(__name__)
ns = api.namespace('recipes', description='Operations related to recipes for a given user')

@ns.route('/')
class RecipeAccountsCollection(Resource):

    @api.expect(recipe)
    def post(self):
        """
        Creates a new user recipe.
        """
        create_recipe(request.json)
        return "Recipe created successfully", 201


@ns.route('/<int:id>')
@api.response(404, 'Recipe not found.')
class RecipeAccount(Resource):

    @api.marshal_with(recipe)
    def get(self, id):
        """
        Returns recipe information.
        """
        return get_recipe(id)

    @api.expect(recipe)
    @api.response(204, 'Recipe successfully updated.')
    def put(self, id):
        """
        Updates recipe information.
        """
        data = request.json
        update_recipe(id, data)
        return None, 204

    @api.response(204, 'Recipe successfully deleted')
    def delete(self, id):
        """
        Deletes a recipe.
        """
        delete_recipe(id)
        return None, 204