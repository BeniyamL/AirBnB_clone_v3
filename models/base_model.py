#!/usr/bin/python3
from datetime import datetime
import uuid
import models
from sqlalchemy import Column, Integer, String, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
import uuid
"""
This module contains the BaseModel class:
All classes should inherit from this class
"""
if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The base class for all storage objects in this project"""
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime(timezone=True), default=datetime.now(),
                            nullable=False)
        updated_at = Column(DateTime(timezone=True), default=datetime.now(),
                            nullable=False,
                            onupdate=datetime.now)

    def __init__(self, *args, **kwargs):
        """
        initialize class object

        **Arguments**
           none: a unique user id and timestamp will be created
           args: a sequence, this should not be used, please pass a dictionary
                 as **dictionary
           kwargs: a dictionay, if the id and timestamp are missing they will
                   be created
        """

        if args:  # this is not the right way to handle kwargs
            kwargs = args[0]
        if kwargs:
            flag_id = False
            flag_created_at = False
            for k in kwargs.keys():
                if k == "created_at" or k == "updated_at":
                    if k == "created_at":
                        flag_created_at = True
                    if not isinstance(kwargs[k], datetime):
                        kwargs[k] = datetime(*self.__str_to_numbers(kwargs[k]))
                elif k == "id":
                    flag_id = True
                setattr(self, k, kwargs[k])
            if not flag_created_at:
                self.created_at = datetime.now()
            if not flag_id:
                self.id = str(uuid.uuid4())
        elif not args:
            self.created_at = datetime.now()
            self.id = str(uuid.uuid4())

    def __str_to_numbers(self, s):
        """
        Prepares a string for datetime

        **Arguments**
           s: a string of numbers
        """
        tmp = ''.join([o if o not in "T;:.,-_" else " " for o in s]).split()
        res = [int(i) for i in tmp]
        return res

    def save(self):
        """method to update self"""
        self.__dict__["updated_at"] = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def __str__(self):
        """edit string representation"""
        return "[{}] ({}) {}".format(type(self)
                                     .__name__, self.id, self.__dict__)

    def to_json(self):
        """convert to json"""
        dupe = self.__dict__.copy()
        dupe.pop('_sa_instance_state', None)

        dupe["created_at"] = dupe["created_at"].isoformat()
        # sqlAlchemy_storage_engine
        if ("updated_at" in dupe):
            dupe["updated_at"] = dupe["updated_at"].isoformat()
        dupe["__class__"] = type(self).__name__
        return dupe
