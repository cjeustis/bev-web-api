import logging
from flask import request
from flask_restplus import Resource, fields
from src.api.users.business import *
from passlib.apps import custom_app_context as pwd_context
from src.api.users.serializers import *
from src.api.restplus import api
from src.database.models import User, Recipe

log = logging.getLogger(__name__)
ns = api.namespace('users', description='Operations related to user accounts')


""" USER """
@ns.route('/register')
@api.response(404, "{'message': 'string'}")
class UserAccountsCollection(Resource):

  @api.expect(user_registration)
  @api.marshal_with(token_response)
  def post(self):
    """
    Creates a new user account.
    """
    return create_user(request.json), 201


@ns.route('/login')
class UserAccountsAuthentication(Resource):

  @api.expect(user_login)
  @api.marshal_with(token_response)
  def post(self):
    """
    Sign in and authenticate a user.
    """
    return authenticate_user(request.json)


@ns.route('/<int:id>')
@api.response(404, "{'message': 'string'}")
@api.header('Auth-Token', 'Authorization token')
class UserAccount(Resource):


  @verify_token
  @api.marshal_with(user_info)
  def get(self, id):
    """
    Returns user account information.
    """
    return get_user(id), 200

  @api.expect(user_registration)
  @api.marshal_with(user_registration)
  @verify_token
  def put(self, id):
    """
    Updates user account information.
    """
    return update_user(id, request.json), 204

  @verify_token
  def delete(self, id):
    """
    Deletes a user account.
    """
    delete_user(id)
    return None, 204

  @ns.route('/<int:id>/logout')
  @api.response(404, "{'message': 'string'}")
  @api.header('Auth-Token', 'Authorization token')
  class UserAccountLogoutCollection(Resource):
    
    @verify_token
    def post(self, id):
      """
      Logs an authenticated user out.
      """
      return unauthenticate_user(id), 200


  @ns.route('/<int:id>/recipes')
  @api.response(404, "{'message': 'string'}")
  @api.header('Auth-Token', 'Authorization token')
  class UserAccountRecipesCollection(Resource):
    
    @api.expect(recipe)
    @api.marshal_with(recipe)
    @verify_token
    def post(self, id):
      """
      Creates a new recipe for a specific user.
      """
      return create_recipe(id, request.json), 201
  
    @api.marshal_with(recipe)
    @verify_token
    def get(self, id):
      """
      Returns all recipes for a user
      """
      return get_all_recipes(id), 201

    @ns.route('/<int:id>/recipes/<int:recipe_id>')
    @api.response(404, "{'message': 'string'}")
    @api.header('Auth-Token', 'Authorization token')
    class UserAccountRecipes(Resource):

      @api.marshal_with(recipe)
      @verify_token
      def get(self, id, recipe_id):
        """
        Returns a specific recipe for a user
        """
        return get_recipe(id, recipe_id), 201

      @api.expect(recipe)
      @api.marshal_with(recipe)
      @verify_token
      def put(self, id, recipe_id):
        """
        Updates information for a specific recipe.
        """
        return update_recipe(id, recipe_id, request.json), 204

      @verify_token
      def delete(self, id, recipe_id):
        """
        Deletes a specific recipe.
        """
        delete_recipe(id, recipe_id)
        return None, 204