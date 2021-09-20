import unittest
import os.path
from os import getenv
from datetime import datetime
from models.base_model import Base
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models.state import State
from models import *


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db', "db")
class Test_DBStorage(unittest.TestCase):
    """
    Test the file storage class
    """
    @classmethod
    def setUpClass(cls):
        """create a session"""
        # close previous connexion to same database
        storage._DBStorage__session.close()
        cls.store = DBStorage()
        test_args = {'updated_at': datetime(2017, 2, 12, 00, 31, 53, 331997),
                     'id': "0234",
                     'created_at': datetime(2017, 2, 12, 00, 31, 53, 331900),
                     'name': 'wifi'}
        cls.model = Amenity(**test_args)
        cls.store.reload()
        cls.test_len = 0

    @classmethod
    def tearDownClass(cls):
        cls.store._DBStorage__session.close()
        storage.reload()

    def test_all(self):
        output = self.store.all('Amenity')
        self.assertEqual(len(output), self.test_len)

    def test_new(self):
        # note: we cannot assume order of test is order written
        self.test_len = len(self.store.all())
        # self.assertEqual(len(self.store.all()), self.test_len)
        self.model.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), self.test_len + 1)
        a = Amenity(name="thing")
        a.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), self.test_len + 2)

    def test_save(self):
        test_len = len(self.store.all())
        a = Amenity(name="another")
        a.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), test_len + 1)
        b = State(name="california")
        self.assertNotEqual(len(self.store.all()), test_len + 2)
        b.save()
        self.store.reload()
        self.assertEqual(len(self.store.all()), test_len + 2)

    def test_reload(self):
        self.model.save()
        a = Amenity(name="different")
        a.save()
        self.store.reload()
        for value in self.store.all().values():
            self.assertIsInstance(value.created_at, datetime)

    def test_get(self):
        """ Test method for get method (retrieve one object) """
        storage = DBStorage()
        test_dct = {"name": 'Jimma'}
        new_obj = State(**test_dct)
        storage.new(new_obj)
        storage.save()
        get_obj = storage.get(State, new_obj.id)
        if get_obj:
            self.assertEqual(get_obj.id, new_obj.id)

    def test_count_classes(self):
        """ Test method for count method(count the number of the given cls) """
        storage = DBStorage()
        for cls in classes.values():
            obj_count = storage.count(cls)
            if obj_count:
                self.assertEqual(len(storage.all(cls)), obj_count)
            else:
                self.assertEqual(len(storage.all(cls)), 0)

    def test_count(self):
        """ Test method for count method(count the number of objects) """
        storage = DBStorage()
        obj_count = storage.count()
        if obj_count:
            self.assertEqual(len(storage.all()), obj_count)
        else:
            self.assertEqual(len(storage.all()), 0)


if __name__ == "__main__":
    unittest.main()
