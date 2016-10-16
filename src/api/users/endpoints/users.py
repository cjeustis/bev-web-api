import logging
from flask import request
from flask_restplus import Resource
from src.api.users.business import create_user, delete_user, update_user
from src.api.users.serializers import user
from src.api.restplus import api
from src.database.models import User

log = logging.getLogger(__name__)
ns = api.namespace('users', description='Operations related to user accounts')

@ns.route('/')
class UserAccountsCollection(Resource):

    @api.expect(user)
    def post(self):
        """
        Creates a new user account.
        """
        create_user(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'User account not found.')
class UserAccount(Resource):

    @api.marshal_with(user)
    def get(self, id):
        """
        Returns user account information.
        """
        return Post.query.filter(Post.id == id).one()

    @api.expect(user)
    @api.response(204, 'User account successfully updated.')
    def put(self, id):
        """
        Updates user account information.
        """
        data = request.json
        update_user(id, data)
        return None, 204

    @api.response(204, 'User account successfully deleted')
    def delete(self, id):
        """
        Deletes a user account.
        """
        delete_user(id)
        return None, 204