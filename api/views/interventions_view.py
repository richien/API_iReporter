from flask.views import MethodView
from flask import jsonify, request
from api.validator import Validate
from api.models.incident_model import Incident
from data import incidents_data


incidents = incidents_data['data']


class InterventionsView(MethodView):

    def post(self):

        request_data = request.get_json()
        error_message = {}
        try:
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
            request_data = request.get_json()
            try:
                if "intervention_id" not in request_data.keys(
                ) or request_data['intervention_id'] != intervention_id:
                    error_message = {
                        'status': 400,
                        'error': "Invalid request - invalid intervention_id supplied or key error in request body"
                    }
                    raise KeyError("Invalid request")
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
                            "message": f"No record  with intervention_id: {intervention_id} was found"
                        }]
                    }
            except KeyError as error:
                error_message.update({"error-type": str(error)})
                return jsonify(error_message), 400
        return jsonify(message), 200
