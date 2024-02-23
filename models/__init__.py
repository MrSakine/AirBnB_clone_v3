#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

if getenv("HBNB_TYPE_STORAGE") == "db":
    CLASSES = db_storage = DBStorage.CLASSES
    storage = DBStorage()
else:
    CLASSES = file_storage = FileStorage.CLASSES
    storage = FileStorage()
storage.reload()

if __name__ != "__main__":
    from models.state import State
    from models.city import City
    from models.user import User
    from models.place import Place
    from models.review import Review
    from models.amenity import Amenity
