from flask import jsonify
import random
from datetime import date
import data

class Incident:

    def __init__(self, id=None, createdOn=None, **kwargs):
        self.id = id or random.randint(10000, 90000)
        self.createdOn = createdOn or date.today()
        self.createdBy = kwargs['createdBy']
        self.type = kwargs['type']
        self.location = kwargs['location']
        self.status = kwargs['status']
        self.comment = kwargs['comment']
        self.images = kwargs['images']
        self.videos = kwargs['videos']
        self.title = kwargs['title']
        
    def to_dict(self):

        incident_dict = {
            'id' : self.id,
            'createdOn' : self.createdOn,
            'createdBy' : self.createdBy,
            'type' : self.type,
            'location' : self.location,
            'status' : self.status,
            'images' : self.images,
            'videos' : self.videos,
            'comment' : self.comment,
            'title' : self.title
        }
        return incident_dict

    def create_incident(self):
        return data.do_create(self.to_dict())

    def update_fields(self, location=None, comment=None):

        if location:
            updated_data = data.update(self.id, location=location)
            if updated_data:
                self.location = location
            return updated_data
        elif comment:
            updated_data = data.update(self.id, comment=comment)
            if updated_data:
                self.comment = comment
            return updated_data

    def delete_incident(self):
        deleted = data.do_delete(self.id)
        if deleted:
            self.to_dict = None
            return deleted
