from flask import jsonify, request, g
from flask.views import MethodView
from flask_jwt import jwt

from api.auth.authenticate import Authenticate
from api.models.database import incidentdb_api
from api.models.incident_model import Incident
from api.validator import Validate


class BaseView(MethodView):
    def __init__(self, type):
        self.type = type

    def get(self, user_id):

        token = Authenticate.retrieve_token_from_request(request)
        error_message = {'status': 400, 'error': ''}
        try:
            is_valid_token = Validate.validate_token(token)
            if  is_valid_token['is_valid']:
                incident_list = []
                incidents = incidentdb_api.get_incidents_by_user(user_id, self.type)
                for data in incidents:
                    incident = Incident(**data)
                    incident_list.append(incident.to_dict())
                            
                if not incident_list:
                    message = {'status': 404, 'data': ["No records found"]}
                else:
                    message = {'status': 200, 'data': incident_list}
                return jsonify(message), message['status']
            else:
                error_message = {
                    'status': is_valid_token['status'],
                    'error': is_valid_token['error']}  
        except Exception as error:
            error_message['error'] = error
        return jsonify(error_message), error_message['status'] 



class UserRedFlagsView(BaseView):
    def __init__(self):
        super().__init__('red-flag')
            

class UserInterventionsView(BaseView):
    def __init__(self):
        super().__init__('intervention')
            
