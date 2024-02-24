#!/usr/bin/python3
"""This module defines a class User"""
import hashlib
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.place import Place
from models.review import Review
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship("Place", cascade="all, delete", backref="user")
    reviews = relationship("Review", cascade="all, delete", backref="user")

    def __init__(self, *args, **kwargs):
        if kwargs:
            if "password" in kwargs:
                self.__hash_password(kwargs["password"])
        super().__init__(*args, **kwargs)

    def __hash_password(self, passw):
        hashed_password = hashlib.md5(passw.encode("utf-8")).hexdigest()
        setattr(self, "password", hashed_password)
