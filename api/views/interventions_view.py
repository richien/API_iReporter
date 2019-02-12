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
                interventions = []
                incidents = incidentdb_api.get_all_intervention_incidents()
                for data in incidents:
                    intervention = Incident(data['incident_id'], data['createdon'], **data)
                    interventions.append(intervention.to_dict())
                            
                if not interventions:
                    message = {'status': 404, 'data': ["No records found"]}
                else:
                    message = {'status': 200, 'data': interventions}
                return jsonify(message), message['status']
            else:
                error_message = {
                    'status': is_valid_token['status'],
                    'error': is_valid_token['error']}
            
        else:
            try:
                intervention = Incident.get_incident(intervention_id)
                is_valid_token = Validate.validate_token(token)
                if  is_valid_token['is_valid'] and not intervention['error']:
                    message = {'status': 200, 'data': [intervention['incident'].to_dict()]}
                    return jsonify(message), message['status']
                else:
                    error_message = {
                    'status': is_valid_token['status'] or intervention['error']['status'],
                    'error': is_valid_token['error'] or intervention['error']['error']}
                    raise Exception
            except Exception as error:
                error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status'] 


    def delete(self, intervention_id):

        token = Authenticate.retrieve_token_from_request(request)
        error_message = {'status': 400}
        try:
            intervention = Incident.get_incident(intervention_id)
            is_valid_token = Validate.validate_token(token)
            if  is_valid_token['is_valid'] and not intervention['error']:
                message = intervention['incident'].delete_incident()
                return jsonify(message), message['status']
            else:
                error_message = {
                    'status': is_valid_token['status'] or intervention['error']['status'],
                    'error': is_valid_token['error'] or intervention['error']['error']}
                raise Exception
        except Exception as error:
            error_message.update({"error-type": str(error)})
        return jsonify(error_message), error_message['status']
