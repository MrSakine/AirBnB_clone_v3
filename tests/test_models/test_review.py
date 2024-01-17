#!/usr/bin/python3
"""
Contains the tests of Review model
"""
from tests.test_models.test_base_model import test_basemodel
from models.review import Review


class test_review(test_basemodel):
    """Class for testing documentation of the Review model"""

    def __init__(self, *args, **kwargs):
        """Initialization of review test"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_docstring(self):
        """Testing docstring"""
        self.assertIsNotNone(Review.__doc__)

    def test_place_id(self):
        """Testing place_id attribute"""
        new = self.value(place_id="")
        self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """Testing user_id attribute"""
        new = self.value(user_id="")
        self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """Testing text attribute"""
        new = self.value(text="")
        self.assertEqual(type(new.text), str)
