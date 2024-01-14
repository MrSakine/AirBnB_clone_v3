#!/usr/bin/python3
"""
Contains the tests of City model
"""
from tests.test_models.test_base_model import test_basemodel
from models.city import City


class test_City(test_basemodel):
    """Class for testing documentation of the City model"""

    def __init__(self, *args, **kwargs):
        """Initialization of city test"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Testing state_id attribute"""
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """Testing name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), str)
