import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os

try:
    from helper.user import User, UsernameLengthError, UsernameFirstError, UsernameLetterError, UsernameCharError
    from helper.database import DatabaseDoesNotContainUsernameError, CosmosHttpResponseErrorMessage
    from helper.api_responses import SuccessfulUserDeletion
except ModuleNotFoundError:
    from api_hub.helper.user import User, UsernameLengthError, UsernameFirstError, UsernameLetterError, UsernameCharError
    from api_hub.helper.database import DatabaseDoesNotContainUsernameError, CosmosHttpResponseErrorMessage
    from api_hub.helper.api_responses import SuccessfulUserDeletion

function = func.Blueprint()

@function.route('userDelete',auth_level=func.AuthLevel.FUNCTION, methods=['DELETE'])
def userDelete(req: func.HttpRequest) -> func.HttpResponse:
    try:
        cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
        database = cosmos.get_database_client(os.environ['DatabaseName'])
        userContainer = database.get_container_client(os.environ['Users_Container'])

        # Get the request
        reqJson = req.get_json()
        logging.info('Python HTTP trigger function processed a request to register a user. JSON: {}'.format(reqJson))

        # Check the database contains the username
        query = "SELECT * FROM p where p.username='{}'".format(reqJson['username'])
        users = list(userContainer.query_items(query=query, enable_cross_partition_query=True))
        if len(users) == 0:
            raise DatabaseDoesNotContainUsernameError


        # Delete the user from the database
        userContainer.delete_item(item=users[0]['id'], partition_key=users[0]['id'])

        # Return the response
        logging.info("User Deleted Successfully")
        return func.HttpResponse(body=json.dumps({'result': True, "msg": SuccessfulUserDeletion()}),
                                 mimetype="application/json")

    except DatabaseDoesNotContainUsernameError:
        message = DatabaseDoesNotContainUsernameError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")

    except CosmosHttpResponseError:
        message = CosmosHttpResponseErrorMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")