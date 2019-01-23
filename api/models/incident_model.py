import random
from datetime import date
import data
from api.models.database import incidentdb_api


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
            'createdBy': self.createdBy,
            'type': self.type,
            'location': self.location,
            'status': self.status,
            'images': self.images,
            'videos': self.videos,
            'comment': self.comment,
            'title': self.title
        }
        return incident_dict

    def create_incident(self):
        return data.do_create(self, self.to_dict())

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
        deleted = data.do_delete(self.id)
        if deleted:
            del self
            return deleted
