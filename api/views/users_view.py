from flask.views import MethodView
from flask import jsonify, request, g
from api.models.user_model import User
from api.auth.authenticate import Authenticate
from api.validator import Validate
from api.models.database import userdb_api
import data

users = data.incidents_data["users"]


class UsersView(MethodView):

    def get(self, user_id=None):

        token = Authenticate.retrieve_token_from_request(request)
        if not user_id:
            is_valid_token = Validate.validate_token(token)
            if  is_valid_token['is_valid'] and g.isAdmin:
                message = User.get_users();
                return jsonify(message), message['status']
            else:
                if is_valid_token['error']:
                    error_message = {
                        'status': is_valid_token['status'],
                        'error': is_valid_token['error']}
                else:
                    error_message = {
                        'status': 401,
                        'error': 'Unauthorized - Cannot access this route'}
        else:
            try:
                user = User.get_user(user_id)
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid'] and not user['error'] and g.isAdmin:
                    message = {'status': 200, 'data': [user['user'].to_dict()]}
                    return jsonify(message), message['status']
                else:
                    error_message = {
                    'status': is_valid_token['status'] or user['error']['status'],
                    'error': is_valid_token['error'] or user['error']['error']}
                    raise Exception
            except Exception as error:
                error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']
