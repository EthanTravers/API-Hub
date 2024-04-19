import unittest
import json
import requests

from api_hub.helper.user import UsernameCharError,UsernameLengthError,UsernameFirstError,UsernameLetterError
from api_hub.tests.TestURLs import TestURLs
from api_hub.helper.api_responses import SuccessfulUserRegister
from api_hub.helper.database import DatabaseContainsUsernameError
class TestUserRegister(unittest.TestCase, TestURLs):

    TEST_URLS = TestURLs.PUBLIC_URLs

    #def setUp(self):

    def tearDown(self):
        requests.delete(self.TEST_URLS['USER_DELETE'],
                        data=json.dumps({"username": TestURLs.DEFAULT_TEST_USER['username']}))
    def testValidUserRegister(self):
        user = TestURLs.DEFAULT_TEST_USER
        response = requests.post(self.TEST_URLS['USER_REGISTER'],
                                 data=json.dumps(user))

        responseOutput = {'result': True, "msg": SuccessfulUserRegister()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 1))

    def testUserAlreadyExists(self):
        user = TestURLs.DEFAULT_TEST_USER
        requests.post(self.TEST_URLS['USER_REGISTER'], data=json.dumps(user))
        response = requests.post(self.TEST_URLS['USER_REGISTER'],data=json.dumps(user))

        responseOutput = {'result': False, "msg": DatabaseContainsUsernameError.getMessage()}
        self.assertEqual(responseOutput, response.json())

    def testInvalidUserRegister_UsernameChar(self):
        user = TestURLs.DEFAULT_TEST_USER
        response = requests.post(self.TEST_URLS['USER_REGISTER'],
                                 data=json.dumps({"username": "Ethan!", "password": "Ethan"}))

        responseOutput = {'result': True, "msg": SuccessfulUserRegister()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 1))