import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os, shutil



try:
    from helper.database import CosmosHttpResponseErrorMessage
    from helper.explorer import scan_python_files
except ModuleNotFoundError:
    from api_hub.helper.database import CosmosHttpResponseErrorMessage
    from api_hub.helper.explorer import scan_python_files

function = func.Blueprint()

@function.route('exploreAPI','req','$return',['POST'],auth_level=func.AuthLevel.FUNCTION)
def exploreAPI(req: func.HttpRequest) -> func.HttpResponse:
    try:
        cosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
        database = cosmos.get_database_client(os.environ['DatabaseName'])
        userContainer = database.get_container_client(os.environ['Users_Container'])
        url = req.get_json()['url']
        logging.info('Python HTTP trigger function processed a request to explore an API: {}'.format(url))

        #Check if uploads folder exists, if not create one
        if not os.path.exists('uploads'):
            # Create the folder if it does not exist
            os.makedirs('uploads')
            logging.info("The 'uploads' folder has been created.")
        else:
            logging.info("The 'uploads' folder already exists.")

        # Get name of API folder (last part of url)
        apiName = url.split('/')[-1]

        if not os.path.exists('uploads/{}'.format(apiName)):

            # Change cwd to uploads
            os.chdir('uploads')

            # Clone the directory if uncloned os.system to call git clone
            os.system("git clone {}".format(url))

            # Change cwd back to parent folder
            os.chdir('..')

        # Parse each file and scan for functions
        routes_info = scan_python_files(apiName)

        for route in routes_info:
            logging.info(f"Function Info: {route}")
            #logging.info(f"Function: {route['function_name']}")
            #logging.info(f"Route Args: {route['route_args']}")
            #logging.info(f"Returns: {route['returns']}\n")
        # Return JSON of functions

        # Delete uploaded API files
        logging.info("Deleting {} files...".format(apiName))
        if os.path.isdir('uploads/{}'.format(apiName)):
            shutil.rmtree('uploads/{}'.format(apiName))

        return func.HttpResponse(body=json.dumps({'result': True, "msg": ""}), mimetype="application/json")
    except CosmosHttpResponseError:
        message = CosmosHttpResponseErrorMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")