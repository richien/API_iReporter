import random
from datetime import date
from api.models.database import incidentdb_api
from api.validator import Validate
from flask import g


class Incident:

    def __init__(self, id=None, createdOn=None, **kwargs):
        self.id = id 
        self.createdOn = createdOn 
        self.createdBy = kwargs['createdby']
        self.type = kwargs['type']
        self.location = kwargs['location']
        self.status = kwargs['status']
        self.comment = kwargs['comment']
        self.images = kwargs['images']
        self.videos = kwargs['videos']
        self.title = kwargs['title']

    def to_dict(self):

        incident_dict = {
            'id': self.id,
            'createdOn': self.createdOn,
            'createdby': self.createdBy,
            'type': self.type,
            'location': self.location,
            'status': self.status,
            'images': self.images,
            'videos': self.videos,
            'comment': self.comment,
            'title': self.title
        }
        return incident_dict

    def update_fields(self, location=None, comment=None):

        if location:
            updated_data = incidentdb_api.update_location(self.id, location=location)
            if updated_data.get('incident_id'):
                self.location = location
            return updated_data
        elif comment:
            updated_data = incidentdb_api.update_comment(self.id, comment=comment)
            if updated_data['incident_id']:
                self.comment = comment
            return updated_data

    def delete_incident(self):
        deleted = incidentdb_api.delete_incident_by_id(self.id)
        if deleted:
            return deleted

    @staticmethod
    def create_incident(data, type):
        try:
            if data['type'].lower() == 'red-flag' and type == 'red-flag':
                red_flag = Incident(**data)
                red_flag_id = incidentdb_api.create_incident(**red_flag.to_dict())
                message = {"status": 201,
                            "data": [{
                                "id": red_flag_id['incident_id'],
                                "message": "Created red-flag record"}]}
                return message
            elif data['type'].lower() == 'intervention' and type == 'intervention':
                intervention = Incident(**data)
                intervention_id = incidentdb_api.create_incident(**intervention.to_dict())
                message = {"status": 201,
                            "data": [{
                                "id": intervention_id['incident_id'],
                                "message": "Created intervention record"}]}
                return message
            else:
                error_message = {'status': 400,
                                 'error': 'Unrecorgnised Incident type'}
                raise Exception('Invalid request field')
        except Exception as error:
            error_message.update({"error-type": str(error)})
            return error_message
    
    @staticmethod
    def get_incident(incident_id):
        incident_obj = None
        error_message = None
        try:
            incident = incidentdb_api.get_incident_by_id(incident_id)
            if incident and incident['incident_id'] == incident_id:
                incident_obj = Incident(
                    incident['incident_id'],
                    incident['createdon'],
                    **incident)              
            if not incident_obj:
                error_message = {
                        "status": 404,
                        "error": "No record  with ID:{0} was found".format(incident_id)}
                raise Exception("Resource Not Found")
        except Exception as error:
            error_message.update({"error-type": str(error)})
        return {'incident': incident_obj, 'error': error_message}

    @staticmethod
    def update_location(data, incident, type):
        if Validate.is_valid_location(data['location']):
            updated_data = incident.update_fields(
                location=data['location'])
            if updated_data:
                message = {
                    "status": 200,
                    "data": [{
                        "id": incident.id,
                        "message": f"Updated {type} record's location",
                        "content": incident.to_dict()
                    }]}
        else:
            message = {
                "status": 400,
                "error": f"Failed to update {type} record's location"}
        return message
    
    @staticmethod
    def update_comment(data, incident, type):
        if not Validate.is_empty_string(data['comment']):
            updated_data = incident.update_fields(
                comment=data['comment'])
            if updated_data:
                message = {
                    "status": 200,
                    "data": [{
                        "id": incident.id,
                        "message": f"Updated {type} record's comment",
                        "content": incident.to_dict()
                    }]}
        else:
            message = {
                "status": 400,
                "error": f"Failed to update {type} record's comment"}
        return message

    @staticmethod
    def update_incident(data, incident, type):
        if g.user_id == incident.createdBy or g.isAdmin == True:
            if 'location' in data.keys():
                message = Incident.update_location(data, incident, type)

            elif 'comment' in data.keys():
                message = Incident.update_comment(data, incident, type)
            else:
                message = {
                    "status": 404,
                    "error": "Resource not found -  Invalid field in request body"}
        else:
            message = {
                'status': 401,
                'error': "Unauthorized: User not authorised to edit incident"
                }
        return message
    
    
            

                        
        
