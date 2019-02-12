from flask import jsonify, request, g
from flask.views import MethodView
from flask_jwt import jwt

from api.auth.authenticate import Authenticate
from api.models.database import incidentdb_api
from api.models.incident_model import Incident
from api.validator import Validate


class BaseView(MethodView):

    def __init__(self, type):
        self.type = type;

    def patch(self, incident_id):

        token = Authenticate.retrieve_token_from_request(request)
        error_message = {'status': 400}
        try:
            validation_result = Validate.validate_request_body(request)
            if validation_result["is_valid"]:
                request_data = request.get_json()
                incident = Incident.get_incident(incident_id)
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid'] and not incident['error']:
                    message = Incident.update_incident(request_data, incident['incident'], self.type)
                    return jsonify(message), message['status']
                else:
                    error_message = {
                    'status': is_valid_token['status'] or incident['error']['status'],
                    'error': is_valid_token['error'] or incident['error']['error']}
                    raise Exception
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
        except ValueError as error:
            error_message.update({"error-type": str(error)})
        except Exception as error:
            error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']


class UpdateRedFlagsLocationView(BaseView):
    def __init__(self):
        super().__init__('red-flag')
            
class UpdateInterventionsLocationView(BaseView):
    def __init__(self):
        super().__init__('intervention')

class UpdateRedFlagsCommentView(BaseView):
    def __init__(self):
        super().__init__('red-flag')            

class UpdateInterventionsCommentView(BaseView):
    def __init__(self):
        super().__init__('intervention')

class UpdateRedFlagStatusView(BaseView):
    def __init__(self):
        super().__init__('red-flag')
            
class UpdateInterventionStatusView(BaseView):
    def __init__(self):
        super().__init__('intervention')

