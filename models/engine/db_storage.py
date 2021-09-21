#!/usr/bin/python3
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import (sessionmaker, scoped_session)
from os import getenv
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
"""
This is the db_storage module
"""
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    __engine = None
    __session = None
    __Session = None

    def __init__(self):
        """
        initializes engine
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')))
        self.__models_available = {"User": User,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        if getenv('HBNB_MYSQL_ENV', 'not') == 'test':
            Base.metadata.drop_all(self.__engine)

    @property
    def available_classes(self):
        """
        Returns Available classes
        """
        return (self.__models_available)

    def all(self, cls=None):
        """
        returns a dictionary of all the class objects
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """
        adds a new obj to the session
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        gets an object of a certain kind of class
        """
        if cls and id:
            if type(cls) is str:
                rqrd_obj = "{}.{}".format(cls, id)
            else:
                rqrd_obj = "{}.{}".format(cls.__name__, id)
            all_cls = self.all(cls)
            return all_cls.get(rqrd_obj)
        return (None)

    def count(self, cls=None):
        """
        counts the number of instances of a class (cls)
        """
        return(len(self.all(cls)))

    def save(self):
        """
        saves the objects fom the current session
        """
        self.__session.commit()

    def reload(self):
        """
        WARNING!!!! I'm not sure if Base.metadata.create_all needs to
        be in the init method
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))

    def delete(self, obj=None):
        """
        deletes an object from the current session
        """
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """
        close a session
        """
        self.__session.remove()
