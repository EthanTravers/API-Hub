import unittest
import json
import requests

from api_hub.helper.user import IncorrectPasswordError, UsernameCharError, UsernameLengthError, UsernameFirstError, \
    UsernameLetterError
from api_hub.tests.TestURLs import TestURLs
from api_hub.helper.api_responses import SuccessfulUserLogin, SuccessfulUserRegister
from api_hub.helper.database import DatabaseDoesNotContainUsernameError, DatabaseContainsUsernameError

TEST_URLS = TestURLs.PUBLIC_URLs


class TestUserLogin(unittest.TestCase, TestURLs):

    def setUp(self):
        requests.post(TEST_URLS['USER_REGISTER'], data=json.dumps(TestURLs.DEFAULT_TEST_USER))

    def tearDown(self):
        requests.delete(TEST_URLS['USER_DELETE'],
                        data=json.dumps({"username": TestURLs.DEFAULT_TEST_USER['username']}))

    def testValidUserLogin(self):
        user = TestURLs.DEFAULT_TEST_USER
        response = requests.post(TEST_URLS['USER_LOGIN'],
                                 data=json.dumps(user))

        responseOutput = {'result': True, "msg": SuccessfulUserLogin()}
        self.assertEqual(responseOutput, response.json())

    def testInvalidUserLogin_IncorrectPassword(self):
        user = TestURLs.DEFAULT_TEST_USER.copy()
        user['password'] = 'ethan'
        response = requests.post(TEST_URLS['USER_LOGIN'],
                                 data=json.dumps(user))

        responseOutput = {'result': False, "msg": IncorrectPasswordError.getMessage()}
        self.assertEqual(responseOutput, response.json())

    def testInvalidUserLogin_UserDoesNotExist(self):
        user = TestURLs.DEFAULT_TEST_USER.copy()
        user['username'] = 'ethan'
        response = requests.post(TEST_URLS['USER_LOGIN'],
                                 data=json.dumps(user))

        responseOutput = {'result': False, "msg": DatabaseDoesNotContainUsernameError.getMessage()}
        self.assertEqual(responseOutput, response.json())


class TestUserRegister(unittest.TestCase, TestURLs):

    def tearDown(self):
        requests.delete(TEST_URLS['USER_DELETE'],
                        data=json.dumps({"username": TestURLs.DEFAULT_TEST_USER['username']}))

    def testValidUserRegister(self):
        user = TestURLs.DEFAULT_TEST_USER
        response = requests.post(TEST_URLS['USER_REGISTER'],
                                 data=json.dumps(user))

        responseOutput = {'result': True, "msg": SuccessfulUserRegister()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 1))

    def testUserAlreadyExists(self):
        user = TestURLs.DEFAULT_TEST_USER
        requests.post(TEST_URLS['USER_REGISTER'], data=json.dumps(user))
        response = requests.post(TEST_URLS['USER_REGISTER'], data=json.dumps(user))

        responseOutput = {'result': False, "msg": DatabaseContainsUsernameError.getMessage()}
        self.assertEqual(responseOutput, response.json())

    def testInvalidUserRegister_UsernameChar(self):
        user = TestURLs.DEFAULT_TEST_USER.copy()
        user['username'] = 'Ethan!'
        print(TestURLs.DEFAULT_TEST_USER['username'])
        response = requests.post(TEST_URLS['USER_REGISTER'],
                                 data=json.dumps(user))

        responseOutput = {'result': False, "msg": UsernameCharError.getMessage()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 0))

    def testInvalidUserRegister_UsernameLength(self):
        user = TestURLs.DEFAULT_TEST_USER.copy()
        user['username'] = 'abcdefghijklmnop'

        response = requests.post(TEST_URLS['USER_REGISTER'],
                                 data=json.dumps(user))

        responseOutput = {'result': False, "msg": UsernameLengthError.getMessage()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 0))

    def testInvalidUserRegister_UsernameFirst(self):
        user = TestURLs.DEFAULT_TEST_USER.copy()
        user['username'] = '_Ethan'

        response = requests.post(TEST_URLS['USER_REGISTER'],
                                 data=json.dumps(user))

        responseOutput = {'result': False, "msg": UsernameFirstError.getMessage()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 0))

    def testInvalidUserRegister_UsernameLetter(self):
        user = TestURLs.DEFAULT_TEST_USER.copy()
        user['username'] = '123'

        response = requests.post(TEST_URLS['USER_REGISTER'],
                                 data=json.dumps(user))

        responseOutput = {'result': False, "msg": UsernameLetterError.getMessage()}
        self.assertEqual(responseOutput, response.json())

        query = "SELECT * FROM p where p.username='{}'".format(user['username'])
        userExists = len(list(self.userContainer.query_items(query=query, enable_cross_partition_query=True)))
        self.assertEqual(True, (userExists == 0))
