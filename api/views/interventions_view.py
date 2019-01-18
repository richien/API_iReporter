from flask.views import MethodView
from flask import jsonify, request
from api.validator import Validate
from api.models.incident_model import Incident
from data import incidents_data


incidents = incidents_data['data']


class InterventionsView(MethodView):

    def post(self):

        try:
            if request.json:
                request_data = request.get_json()
                validation_result = Validate.validate_incident_post_request(
                    request_data)
                if validation_result["is_valid"]:
                    if request_data['type'].lower() == 'intervention':
                        intervention = Incident(**request_data)
                        incidents.append(intervention.to_dict())
                        intervention_id = intervention.id
                        message = {
                            'status': 201,
                            'data': [{
                                'id': intervention_id,
                                'message': 'Created intervention record'
                            }]
                        }
                        return jsonify(message), 201
                    else:
                        error_message = {
                            'status': 400,
                            'error': 'Type field should be intervention'}
                        raise Exception('Invalid request field')
                else:
                    error_message = validation_result['message']
                    raise Exception("Validation Error")
            else:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"}
                raise ValueError('Empty request body')
        except ValueError as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return jsonify(error_message), error_message['status']

    def get(self, intervention_id):
        if not intervention_id:
            interventions = []
            for data in incidents:
                if data['type'].lower() == 'intervention':
                    intervention = Incident(**data)
                    interventions.append(intervention.to_dict())
            if not interventions:
                message = {'status': 200, 'data': ["No records found"]}
            else:
                message = {'status': 200, 'data': interventions}
        else:
            try:
                intervention = None
                for index, data in enumerate(incidents):
                    if incidents[index]['id'] == intervention_id:
                        intervention = Incident(**data)
                if intervention:
                    message = {
                        "status": 200,
                        "data": [{
                            "id": intervention.id,
                            "message": intervention.to_dict()
                        }]
                    }
                else:
                    message = {
                        'status': 200,
                        'data': [{
                            "id": intervention_id,
                            "message": f"No record  with ID: {intervention_id} was found"
                        }]
                    }
            except Exception as error:
                error_message = {
                    'status': 400,
                    'error': error}
                return jsonify(error_message), error_message['status']
        return jsonify(message), message['status']
