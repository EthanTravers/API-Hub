import json
import os
import unittest

from azure.cosmos import CosmosClient


def _loadEnvFromJson():
    local_settings_json = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'local.settings.json')
    if os.path.exists(local_settings_json):
        with open(local_settings_json) as f:
            settings = json.load(f)
        os.environ.update(settings['Values'])
    else:
        raise FileNotFoundError("local.settings.json not found")

class TestURLs:
    _loadEnvFromJson()

    key = os.environ["FunctionAppKey"]
    cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
    database = cosmos.get_database_client(os.environ['DatabaseName'])
    userContainer = database.get_container_client(os.environ['Users_Container'])

    # Public URLs
    PUBLIC_URLs = {
        "USER_REGISTER": "https://apihub-et2g21.azurewebsites.net/api/userregister?code={}".format(key),
        "USER_DELETE": "https://apihub-et2g21.azurewebsites.net/api/userDelete?code={}".format(key),
        "USER_LOGIN": "https://apihub-et2g21.azurewebsites.net/api/userLogin?code={}".format(key),
    }
    # Local URLs
    LOCAL_URLs = {
        "USER_REGISTER": "http://localhost:7071/api/userRegister?code={}".format(key),
        "USER_DELETE": "http://localhost:7071/api/userDelete?code={}".format(key),
        "USER_LOGIN": "http://localhost:7071/api/userLogin?code={}".format(key),
    }

    DEFAULT_TEST_USER = {
        "username":"Ethan",
        "password":"Ethan"
    }
