#!/usr/bin/python3
"""DATABASE engine"""
import shlex
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Database engine"""

    CLASSES = {
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    __engine = None
    __session = None

    def __init__(self):
        """init"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True,
        )

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """get all objects"""
        my_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for q in query:
                key = "{}.{}".format(type(q).__name__, q.id)
                my_dict[key] = q
        else:
            class_list = [State, City, Place, Amenity, Review, User]
            for c in class_list:
                query = self.__session.query(c)
                for q in query:
                    key = "{}.{}".format(type(q).__name__, q.id)
                    my_dict[key] = q
        return my_dict

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
        return self.all(cls).get(name)

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
            query = self.__session.query(cls)
            count = len([i for i in query])
        else:
            class_list = [State, City, Place, Amenity, Review, User]
            for c in class_list:
                query = self.__session.query(c)
                count += len([i for i in query])
        return count

    def new(self, obj):
        """add new element"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """save changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete element"""
        if obj:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id
            ).delete()

    def reload(self):
        """reload"""
        Base.metadata.create_all(self.__engine)
        make_session = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(make_session)
        self.__session = Session()

    def close(self):
        """close Session"""
        self.__session.close()
