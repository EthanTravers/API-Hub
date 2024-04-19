import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os

try:
    from helper.user import User, UsernameLengthError, UsernameFirstError, UsernameLetterError, UsernameCharError
    from helper.database import DatabaseContainsUsernameError, CosmosHttpResponseErrorMessage
    from helper.api_responses import SuccessfulUserRegister
except ModuleNotFoundError:
    from api_hub.helper.user import User, UsernameLengthError, UsernameFirstError, UsernameLetterError, UsernameCharError
    from api_hub.helper.database import DatabaseContainsUsernameError, CosmosHttpResponseErrorMessage
    from api_hub.helper.api_responses import SuccessfulUserRegister

function = func.Blueprint()
 
@function.route('userRegister',auth_level=func.AuthLevel.FUNCTION, methods=['POST'])
def userRegister(req: func.HttpRequest) -> func.HttpResponse:
    try:
        cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
        database = cosmos.get_database_client(os.environ['DatabaseName'])
        userContainer = database.get_container_client(os.environ['Users_Container'])

        # Get the request
        reqJson = req.get_json()
        logging.info('Python HTTP trigger function processed a request to register a user. JSON: {}'.format(reqJson))

        # Check the username and password are valid
        user = User(reqJson)
        user.CheckUsernameValid()
        #user.CheckPasswordValid()

        # Check the database does NOT contain the username already
        query = "SELECT * FROM p where p.username='{}'".format(reqJson['username'])
        usernameExists = len(list(userContainer.query_items(query=query, enable_cross_partition_query=True))) != 0
        if usernameExists:
            raise DatabaseContainsUsernameError

        # Add the user to the database
        userContainer.create_item(body=reqJson, enable_automatic_id_generation=True)

        # Return the response
        logging.info("User Added Successfully")
        return func.HttpResponse(body=json.dumps({'result': True, "msg": SuccessfulUserRegister()}), mimetype="application/json")

    except UsernameLetterError:
        message = UsernameLetterError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")

    except UsernameCharError:
        message = UsernameCharError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")

    except UsernameFirstError:
        message = UsernameFirstError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")

    except UsernameLengthError:
        message = UsernameLengthError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")

    except DatabaseContainsUsernameError:
        message = DatabaseContainsUsernameError.getMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")

    except CosmosHttpResponseError:
        message = CosmosHttpResponseErrorMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")
