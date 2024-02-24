#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import shlex
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    CLASSES = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage

        Args:
            - cls (class, optional): the class to fetch from @__objects
        """
        dicts = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace(".", " ")
                partition = shlex.split(partition)
                if partition[0] == cls.__name__:
                    dicts[key] = self.__objects[key]
            return dicts
        else:
            return self.__objects

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID, or None if not found

        Args:
            - cls (class): the class to fetch
            - id (str): representing the object ID
        """
        if type(cls) is str:
            cls = eval(cls)
        name = "{0}.{1}".format(cls.__name__, id)
        return self.__objects.get(name)

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class
        If no class is passed, returns the count of all objects in storage

        Args:
            - cls (class): the class to count
        """
        count = 0
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            dictionary = self.__objects
            for key in dictionary:
                partition = key.replace(".", " ")
                partition = shlex.split(partition)
                if partition[0] == cls.__name__:
                    count += 1
            return count
        else:
            return len(self.__objects)

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update(
            {obj.to_dict()["__class__"] + "." + obj.id: obj}
        )

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict(include_password=True)
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete obj from @__objects if its inside

        Args:
            - obj (object, optional): the object to delete from @__objects
        """
        if obj:
            try:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                del self.__objects[key]
            except (KeyError, AttributeError):
                pass

    def close(self):
        """Call the reload method."""
        self.reload()
