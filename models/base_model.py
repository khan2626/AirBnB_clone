#!/usr/bin/python3
"""It defines a Base class"""
import models
from datetime import datetime
from uuid import uuid4

class BaseModel:
    """It reprsents a BaseModel class"""
    def __init__(self, *args, **kwargs):
        """It initializes a new BaseModel"""
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        dt_format = "%Y-%m-%dT%H:%S.%f"
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, dt_format)
                else:
                    self.__dict__[key] = value
            else:
                models.storage.new(self)

    def save(self):
        """it updates updated_at with current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns all key/value of __dict__"""
        dict = self.__dict__.copy()
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        dict["__class__"] = self.__class__.__name__
        return dict
    def __str__(self):
        """it prints str representation of BaseModel instance"""
        class_name = self.__class__.__name__

        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
