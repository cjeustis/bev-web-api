import logging
from flask import request
from flask_restplus import Resource, fields
from src.api.users.business import *
from src.api.users.serializers import user, recipe
from src.api.restplus import api
from src.database.models import User, Recipe

log = logging.getLogger(__name__)
ns = api.namespace('users', description='Operations related to user accounts')

""" USER """
@ns.route('/')
class UserAccountsCollection(Resource):

  @api.expect(user)
  @api.marshal_with(user)
  @api.response(404, "{'message': 'string'}")
  def post(self):
    """
    Creates a new user account.
    """
    return create_user(request.json), 201


@ns.route('/<int:id>')
@api.response(404, "{'message': 'string'}")
class UserAccount(Resource):

  @api.marshal_with(user)
  def get(self, id):
    """
    Returns user account information.
    """
    return get_user(id), 200

  @api.expect(user)
  @api.marshal_with(user)
  def put(self, id):
    """
    Updates user account information.
    """
    return update_user(id, request.json), 204

  def delete(self, id):
    """
    Deletes a user account.
    """
    delete_user(id)
    return None, 204

  @ns.route('/<int:id>/recipes')
  @api.response(404, "{'message': 'string'}")
  class UserAccountRecipesCollection(Resource):
    
    @api.expect(recipe)
    @api.marshal_with(recipe)
    def post(self, id):
      """
      Creates a new recipe for a specific user.
      """
      return create_recipe(id, request.json), 201
  
    @api.marshal_with(recipe)
    def get(self, id):
      """
      Returns all recipes for a user
      """
      return get_all_recipes(id), 201

    @ns.route('/<int:id>/recipes/<int:recipe_id>')
    @api.response(404, "{'message': 'string'}")
    class UserAccountRecipes(Resource):

      @api.marshal_with(recipe)
      def get(self, id, recipe_id):
        """
        Returns all recipes for a user
        """
        return get_recipe(id, recipe_id)

      @api.expect(recipe)
      @api.marshal_with(recipe)
      def put(self, id, recipe_id):
        """
        Updates information for a specific recipe.
        """
        return update_recipe(id, recipe_id, request.json), 204

      def delete(self, id, recipe_id):
        """
        Deletes a specific recipe.
        """
        delete_recipe(id, recipe_id)
        return None, 204




# """ USER RECIPES """
# @ns.route('/<int:id>')
# @api.response(404, "{'message': 'string'}")
# class UserAccountsRecipesCollection(Resource):
  
#   @api.expect(recipe)
#   @api.marshal_with(recipe)
#   def post(self):
#     """
#     Creates a new recipe for a specific user.
#     """
#     # return create_recipe(user_id, request.json), 201

#   @api.marshal_with(recipe)
#   def get(self):
#     """
#     Return all recipes for a specific user.
#     """
#     return None, 201
#     # return get_all_recipes(user_id), 201


# @ns.route('/recipes/<int:user_id>/<int:recipe_id>')
# @api.response(404, "{'message': 'string'}")
# class UserAccountRecipe(Resource):

#   @api.marshal_with(recipe)
#   def get(self, id):
#     """
#     Returns a specific recipe associeted with a user.
#     """
#     return get_recipe(user_id, recipe_id), 200

#   @api.expect(recipe)
#   @api.marshal_with(recipe)
#   def put(self, id):
#     """
#     Updates information about a specific recipe.
#     """
#     data = request.json
#     return update_recipe(user_id, recipe_id, data), 204

#   def delete(self, id):
#     """
#     Deletes a specific recipe.
#     """
#     delete_recipe(user_id, recipe_id)
#     return None, 204