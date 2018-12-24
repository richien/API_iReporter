from flask import jsonify
import random
from datetime import date

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
        indent_dict = {
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
        return indent_dict