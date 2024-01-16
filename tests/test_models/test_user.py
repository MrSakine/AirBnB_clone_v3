#!/usr/bin/python3
"""
Contains the tests of User model
"""
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """Class for testing documentation of the User model"""

    def __init__(self, *args, **kwargs):
        """Initialization of user test"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Testing first_name attribute"""
        new = self.value(first_name="")
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """Testing last_name attribute"""
        new = self.value(last_name="")
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """Testing email attribute"""
        new = self.value(email="")
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """Testing password attribute"""
        new = self.value(password="")
        self.assertEqual(type(new.password), str)
