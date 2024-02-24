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
    places = relationship(
        "Place", cascade="all, delete", backref="user"
    )
    reviews = relationship(
        "Review", cascade="all, delete", backref="user"
    )

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            password = str(kwargs.pop("password"))
            md = hashlib.md5()
            md.update(str.encode(password))
            hashed_password = md.hexdigest()
            kwargs["password"] = hashed_password
        super().__init__(*args, **kwargs)
