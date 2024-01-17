#!/usr/bin/python3
"""
Contains the tests of Base model
"""
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") == "db", "basemodel not supported"
)
class test_basemodel(unittest.TestCase):
    """Class for testing documentation of the Base model"""

    def __init__(self, *args, **kwargs):
        """Initialization of the class"""
        super().__init__(*args, **kwargs)
        self.name = "BaseModel"
        self.value = BaseModel

    def setUp(self):
        """Set up base model tests"""
        pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_default(self):
        """Default test"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Keyword argument tests"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """TypeError when keyword argument is an integer"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Testing save"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open("file.json", "r") as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Testing string representation"""
        i = self.value()
        self.assertEqual(
            str(i), "[{}] ({}) {}".format(self.name, i.id, i.__dict__)
        )

    def test_todict(self):
        """Testing to_dict method"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Testing keyword argument is none"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Testing one keyword argument"""
        n = {"Name": "test"}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """Testing id attribute"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Testing created_at attribute"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Testing updated_at attribute"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
