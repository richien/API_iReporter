from flask.views import MethodView
from flask import jsonify, request
from api.validator import Validate
from api.models.incident_model import Incident
from api.models.database import incidentdb_api


from data import incidents_data


incidents = incidents_data['data']


class InterventionsView(MethodView):

    def post(self):

        try:
            error_message = {'status': 500}
            if request.json:
                request_data = request.get_json()
                validation_result = Validate.validate_incident_post_request(
                    request_data)
            else:
                error_message = {
                    'status': 400,
                    'error': "Invalid request - request body cannot be empty"}
                raise ValueError("Empty request body")
            if validation_result["is_valid"]:
                if request_data['type'].lower() == 'intervention':
                    intervention = Incident(**request_data)
                    intervention = incidentdb_api.create_incident(**intervention.to_dict())
                    message = {"status": 201,
                                "data": [{
                                    "id": intervention['incident_id'],
                                            "message": "Created intervention record"
                                            }]
                                }
                    return jsonify(message), message['status']
                else:
                    error_message = {'status': 400,
                                     'error': 'Type field should be intervention'}
                    raise Exception('Invalid request field')
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
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
