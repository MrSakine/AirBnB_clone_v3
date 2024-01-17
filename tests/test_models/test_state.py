#!/usr/bin/python3
"""
Contains the tests of State model
"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """Class for testing documentation of the State model"""

    def __init__(self, *args, **kwargs):
        """Initialization of state test"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_docstring(self):
        """Testing docstring"""
        self.assertIsNotNone(State.__doc__)

    def test_name3(self):
        """Testing name attribute"""
        new = self.value(name="")
        self.assertEqual(type(new.name), str)
