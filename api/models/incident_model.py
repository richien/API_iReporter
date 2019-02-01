import random
from datetime import date
from api.models.database import incidentdb_api
from flask import jsonify


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
    def createIncident(data, type):
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
