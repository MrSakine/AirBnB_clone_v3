#!/usr/bin/python3
"""
Contains the tests of Amenity model
"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity


class test_Amenity(test_basemodel):
    """Class for testing documentation of the Amenity model"""

    def __init__(self, *args, **kwargs):
        """Initialization of the class test_Amenity"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test to check the type of the attribute name"""
        new = self.value()
        self.assertEqual(type(new.name), str)
