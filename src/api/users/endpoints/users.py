import logging
from flask import request
from flask_restplus import Resource, fields
from src.api.users.business import create_user, get_user, delete_user, update_user
from src.api.users.serializers import user
from src.api.restplus import api
from src.database.models import User

log = logging.getLogger(__name__)
ns = api.namespace('users', description='Operations related to user accounts')


@ns.route('/')
class UserAccountsCollection(Resource):

    @api.expect(user)
    @api.marshal_with(user)
    def post(self):
        """
        Creates a new user account.
        """
        return create_user(request.json), 201


@ns.route('/<int:id>')
@api.response(404, 'User account not found.')
class UserAccount(Resource):

    @api.marshal_with(user)
    @api.response(204, 'User account exists')
    def get(self, id):
        """
        Returns user account information.
        """
        return get_user(id), 200

    @api.expect(user)
    @api.marshal_with(user)
    @api.response(204, 'User account successfully updated.')
    def put(self, id):
        """
        Updates user account information.
        """
        data = request.json
        return update_user(id, data), 204

    @api.response(204, 'User account successfully deleted')
    def delete(self, id):
        """
        Deletes a user account.
        """
        delete_user(id)
        return None, 204