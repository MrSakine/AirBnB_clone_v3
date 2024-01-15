#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(
        String(60), unique=True, nullable=False, primary_key=True
    )
    updated_at = Column(
        DATETIME, nullable=False, default=datetime.utcnow()
    )
    created_at = Column(
        DATETIME, nullable=False, default=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage

            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            keys = ["created_at", "updated_at"]
            for key in kwargs:
                if key in keys:
                    setattr(
                        self, key, datetime.fromisoformat(kwargs[key])
                    )
                elif key != "__class__":
                    setattr(self, key, kwargs[key])
            if getenv("HBNB_TYPE_STORAGE") == "db":
                if not hasattr(kwargs, "id"):
                    setattr(self, "id", str(uuid.uuid4()))
                if not hasattr(kwargs, "created_at"):
                    setattr(self, "created_at", datetime.now())
                if not hasattr(kwargs, "created_at"):
                    setattr(self, "updated_at", datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()

        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]

        dictionary.update(
            {
                "__class__": (str(type(self)).split(".")[-1]).split(
                    "'"
                )[0]
            }
        )

        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage

        storage.delete(self)
