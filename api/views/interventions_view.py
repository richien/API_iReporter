from flask.views import MethodView
from flask import jsonify, request
from flask_jwt import jwt
from api.validator import Validate
from api.models.incident_model import Incident
from api.models.database import incidentdb_api
from api.auth.authenticate import Authenticate


class InterventionsView(MethodView):

    def post(self):

        token = Authenticate.retrieve_token_from_request(request)
        error_message = {'status': 400}
        try:
            validation_result = Validate.validate_request(request)
            if validation_result["is_valid"]:
                request_data = request.get_json()
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid']:
                    message = Incident.create_incident(request_data, 'intervention')
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


    def get(self, intervention_id):

        token = Authenticate.retrieve_token_from_request(request)
        
        if not intervention_id:
            is_valid_token = Validate.validate_token(token)
            if  is_valid_token['is_valid']:
                red_flags = []
                incidents = incidentdb_api.get_all_intervention_incidents()
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
                red_flag = Incident.get_incident(intervention_id)
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

    def patch(self, intervention_id):

        try:
            if not request.json:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"
                }
                raise ValueError("Empty request body")

            request_data = request.get_json()
            intervention = None
            incident = incidentdb_api.get_incident_by_id(intervention_id)
            if incident and incident['incident_id'] == intervention_id:
                    intervention = Incident(
                        incident['incident_id'], 
                        incident['createdon'], 
                        **incident)                   
            if not intervention:
                error_message = {
                    "status": 404,
                    "error": "No record  with ID:{0} was found".format(intervention_id)}
                raise Exception("Resource Not Found")
            if 'location' in request_data.keys():
                if Validate.is_valid_location(request_data['location']):
                    updated_data = intervention.update_fields(
                        location=request_data['location'])
                    if updated_data:
                        message = {
                            "status": 200,
                            "data": [{
                                "id": intervention_id,
                                "message": "Updated intervention record's location",
                                "content": intervention.to_dict()
                            }]
                        }
                else:
                    message = {
                        "status": 400,
                        "error": "Failed to update intervention record's location"
                    }
            elif 'comment' in request_data.keys():
                if not Validate.is_empty_string(request_data['comment']):
                    updated_data = intervention.update_fields(
                        comment=request_data['comment'])
                    if updated_data:
                        message = {
                            "status": 200,
                            "data": [{
                                "id": intervention_id,
                                "message": "Updated intervention record's comment",
                                "content": intervention.to_dict()
                            }]
                        }
                else:
                    message = {
                        "status": 400,
                        "error": "Failed to update intervention record's comment"
                    }
            else:
                message = {
                    "status": 404,
                    "error": "Resource not found -  Invalid field in request body"}
            return jsonify(message), message['status']
        except ValueError as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
