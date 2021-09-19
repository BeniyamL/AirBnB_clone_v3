#!/usr/bin/python3
import models
from models.base_model import BaseModel, Base, Table, Column, String
from sqlalchemy import ForeignKey
from os import getenv
"""
city module
    contains
        the City class inherts from BaseModel, Base
"""


class City(BaseModel, Base):
    """
    The City class
    """
    if getenv('HBNB_TYPE_STORAGE', 'fs') == 'db':
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes from BaseModel
        """
        super().__init__(*args, **kwargs)

    @property
    def places(self):
        """
        returns all places in a city
        """
        all_places = models.storage.all('Place').values()
        result = [place for place in all_places if place.city_id == self.id]
        return (result)
