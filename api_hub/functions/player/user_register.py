import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os

function = func.Blueprint()

@function.route('userRegister',auth_level=func.AuthLevel.FUNCTION, methods=['POST'])
def userRegister(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(body=json.dumps({'result':True}),mimetype='application/json')