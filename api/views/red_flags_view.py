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
                    message = {'status': 200, 'data': ["No records found"]}
                else:
                    message = {'status': 200, 'data': red_flags}
            else:
                error_message = {
                    'status': is_valid_token['status'],
                    'error': is_valid_token['error']
                }
                return jsonify(error_message), error_message['status']
            
        else:
            try:
                red_flag = None
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid']:
                    incident = incidentdb_api.get_incident_by_id(red_flag_id)
                    if incident and incident['incident_id'] == red_flag_id:
                            red_flag = Incident(incident['incident_id'], incident['createdon'], **incident)
                    if red_flag:
                        message = {
                            "status": 200,
                            "data": [red_flag.to_dict()]
                        }
                    else:
                        message = {
                            'status': 200,
                            'data': [{
                                "id": red_flag_id,
                                "message": f"No record  with ID:{red_flag_id} was found"
                            }]
                        }
                else:
                    error_message = {
                    'status': is_valid_token['status'],
                    'error': is_valid_token['error']
                    }
                    raise jwt.InvalidTokenError('Unauthorized')
            except jwt.InvalidTokenError as error:
                error_message.update({'error-type': str(error)})
                return jsonify(error_message), error_message['status']
            except Exception as error:
                error_message = {
                    'status': 400,
                    'error': error
                }
                return jsonify(error_message), error_message['status']
        
        return jsonify(message), message['status']

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
                    'error': is_valid_token['error']
                    }
                    raise jwt.InvalidTokenError('Unauthorized')
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
        except jwt.InvalidTokenError as error:
            error_message.update({'error-type': str(error)})
        except Exception as error:
            error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']

    def patch(self, red_flag_id):

        error_message = {'status': 400}
        try:
            validation_result = Validate.validate_request_body(request)
            if validation_result["is_valid"]:
                request_data = request.get_json()
                red_flag = Incident.get_incident(red_flag_id)
                if 'location' in request_data.keys():
                    message = Incident.update_location(request_data, red_flag, 'red-flag')

                elif 'comment' in request_data.keys():
                    message = Incident.update_comment(request_data, red_flag, 'red-flag')
                else:
                    message = {
                        "status": 404,
                        "error": "Resource not found -  Invalid field in request body"}
                return jsonify(message), message['status']
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
        except ValueError as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']

    def delete(self, red_flag_id):

        try:
            red_flag = None
            incident = incidentdb_api.get_incident_by_id(red_flag_id)
            if incident:
                red_flag = Incident(
                        incident['incident_id'], 
                        incident['createdon'], 
                        **incident)
            if not red_flag:
                error_message = {
                    "status": 404,
                    "error": "No record  with ID:{0} was found".format(red_flag_id)}
                raise Exception("Record not found")
            else:
                red_flag.delete_incident()
                message = {
                    "status": 200,
                    "data": [{
                        "id": red_flag_id,
                        "message": "Red-flag record deleted",
                    }]
                }
            return jsonify(message), message['status']
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
