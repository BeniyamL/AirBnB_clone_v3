#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city import City

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("state id: {}".format(first_state_id))
print("First state: {}".format(storage.get(State, first_state_id)))


print("All objects: {}".format(storage.count()))
print("City objects: {}".format(storage.count(City)))

first_state_id = list(storage.all(City).values())[0].id
print("city id: {}".format(first_state_id))
print("First city: {}".format(storage.get(City, first_state_id)))
