import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os

try:
    from helper.user import IncorrectPasswordError
    from helper.database import CosmosHttpResponseErrorMessage,DatabaseDoesNotContainUsernameError
    from helper.api_responses import SuccessfulUserLogin
except ModuleNotFoundError:
    from api_hub.helper.user import IncorrectPasswordError
    from api_hub.helper.database import CosmosHttpResponseErrorMessage,DatabaseDoesNotContainUsernameError
    from api_hub.helper.api_responses import SuccessfulUserLogin

function = func.Blueprint()

@function.route('userLogin',auth_level=func.AuthLevel.FUNCTION, methods=['POST'])
def userLogin(req: func.HttpRequest) -> func.HttpResponse:
    try:
        cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
        database = cosmos.get_database_client(os.environ['DatabaseName'])
        userContainer = database.get_container_client(os.environ['Users_Container'])

        # Get the request
        reqJson = req.get_json()
        logging.info('Python HTTP trigger function processed a request to register a user. JSON: {}'.format(reqJson))

        # Get user data from the input username
        query = "SELECT * FROM p where p.username='{}'".format(reqJson['username'])
        userInfoList = list(userContainer.query_items(query=query, enable_cross_partition_query=True))
        if len(userInfoList) != 1:
            raise DatabaseDoesNotContainUsernameError
        userInfo = userInfoList[0]
        if reqJson['password'] != userInfo['password']:
            raise IncorrectPasswordError

        return func.HttpResponse(body=json.dumps({'result':True,"msg": SuccessfulUserLogin()}),mimetype='application/json')

    except DatabaseDoesNotContainUsernameError:
        message = DatabaseDoesNotContainUsernameError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False,"msg": message}),mimetype='application/json')

    except IncorrectPasswordError:
        message = IncorrectPasswordError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False,'msg':message}))

    except CosmosHttpResponseError:
        message = CosmosHttpResponseErrorMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")