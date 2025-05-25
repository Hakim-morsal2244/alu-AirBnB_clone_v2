#!/usr/bin/python3
"""Test DBStorage"""
import unittest
import os
from models.engine.db_storage import DBStorage
from models.state import State
from models import storage

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not using db")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage"""

    def test_new_and_save(self):
        """Test new() and save() methods"""
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertIn(state.id, [s.id for s in storage.all(State).values()])

if __name__ == "__main__":
    unittest.main()
