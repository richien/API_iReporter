from flask.views import MethodView
from flask import jsonify, request
from api.views.validator import Validate
from api.models.incident_model import Incident
from data import incidents_data


incidents = incidents_data['data']


class InterventionsView(MethodView):
    
    def post(self):
        
        request_data = request.get_json()
        error_message = {}
        try:
            validation_result = Validate.validate_incident_post_request(request_data)
            if validation_result["is_valid"]:
                intervention = Incident(**request_data)
                incidents.append(intervention.to_dict())
                intervention_id = intervention.id
                message = {
                    'status' : 201,
                    'data' : [{
                        'id' : intervention_id,
                        'message' : 'Created intervention record'
                    }]
                }
                return jsonify(message), 201
            else:
                error_message = validation_result['message']
                raise Exception("Validation Error")
        except Exception as error: 
            error_message.update({"error-type":str(error)})  
            return jsonify(error_message), 400