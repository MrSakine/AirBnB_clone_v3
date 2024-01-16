#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv
import models
import shlex


class State(BaseModel, Base):
    """State class / table model"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def cities(self):
            """The cities property"""
            all_storage = models.storage.all()
            elements = []
            result = []
            for key in all_storage:
                city = key.replace(".", " ")
                city = shlex.split(city)
                if city[0] == "City":
                    elements.append(all_storage[key])
            for e in elements:
                if e.state_id == self.id:
                    result.append(e)
            return result
