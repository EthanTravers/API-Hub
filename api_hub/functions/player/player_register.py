import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os

try:
    from functions.helper.player import Player, UsernameLengthError, PasswordLengthError
    from functions.helper.exceptions import DatabaseContainsUsernameError, CosmosHttpResponseErrorMessage
except ModuleNotFoundError:
    from api_hub.functions.helper.player import Player, UsernameLengthError, PasswordLengthError
    from api_hub.functions.helper.exceptions import DatabaseContainsUsernameError, CosmosHttpResponseErrorMessage

function = func.Blueprint()

@function.route('playerRegister',auth_level=func.AuthLevel.FUNCTION, methods=['POST'])
def playerRegister(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(body=json.dumps({'result':True}),mimetype='application/json')