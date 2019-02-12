from flask import jsonify, request, g
from flask.views import MethodView
from flask_jwt import jwt

from api.auth.authenticate import Authenticate
from api.models.database import incidentdb_api
from api.models.incident_model import Incident
from api.validator import Validate


class RedFlagsView(MethodView):

    def get(self, red_flag_id):

        token = Authenticate.retrieve_token_from_request(request)
        
        if not red_flag_id:
            is_valid_token = Validate.validate_token(token)
            if  is_valid_token['is_valid']:
                red_flags = []
                incidents = incidentdb_api.get_all_redflag_incidents()
                for data in incidents:
                    red_flag = Incident(data['incident_id'], data['createdon'], **data)
                    red_flags.append(red_flag.to_dict())
                            
                if not red_flags:
                    message = {'status': 404, 'data': ["No records found"]}
                else:
                    message = {'status': 200, 'data': red_flags}
                return jsonify(message), message['status']
            else:
                error_message = {
                    'status': is_valid_token['status'],
                    'error': is_valid_token['error']}
            
        else:
            try:
                red_flag = Incident.get_incident(red_flag_id)
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid'] and not red_flag['error']:
                    message = {'status': 200, 'data': [red_flag['incident'].to_dict()]}
                    return jsonify(message), message['status']
                else:
                    error_message = {
                    'status': is_valid_token['status'] or red_flag['error']['status'],
                    'error': is_valid_token['error'] or red_flag['error']['error']}
                    raise Exception
            except Exception as error:
                error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']       
            

    def post(self):

        token = Authenticate.retrieve_token_from_request(request)
        error_message = {'status': 400}
        try:
            validation_result = Validate.validate_request(request)
            if validation_result["is_valid"]:
                request_data = request.get_json()
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid']:
                    message = Incident.create_incident(request_data, 'red-flag')
                    return jsonify(message), message['status']
                else:
                    error_message = {
                    'status': is_valid_token['status'],
                    'error': is_valid_token['error']}
                    raise jwt.InvalidTokenError('Unauthorized')
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
        except jwt.InvalidTokenError as error:
            error_message.update({'error-type': str(error)})
        except Exception as error:
            error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']

    def delete(self, red_flag_id):

        token = Authenticate.retrieve_token_from_request(request)
        error_message = {'status': 400}
        try:
            red_flag = Incident.get_incident(red_flag_id)
            is_valid_token = Validate.validate_token(token)
            if  is_valid_token['is_valid'] and not red_flag['error']:
                red_flag['incident'].delete_incident()
                message = red_flag['incident'].delete_incident()
                return jsonify(message), message['status']
            else:
                error_message = {
                    'status': is_valid_token['status'] or red_flag['error']['status'],
                    'error': is_valid_token['error'] or red_flag['error']['error']}
                raise Exception
        except Exception as error:
            error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']
