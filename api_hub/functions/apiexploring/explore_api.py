import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError

import json, logging, os, shutil, subprocess



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

        if not os.path.exists(f'uploads/{apiName}'):
            # Change cwd to 'uploads'
            os.chdir('uploads')

            # Verify if the URL can be cloned by trying a dry run of git clone
            try:
                # Using subprocess.run to run the git clone command and capture the return code
                result = subprocess.run(["git", "clone", url], capture_output=True, text=True)

                if result.returncode == 0:
                    logging.info(f"Successfully cloned the repository: {url}")
                else:
                    logging.info(f"Failed to clone the repository: {url}")
                    logging.info(f"Error message: {result.stderr}")
                    return func.HttpResponse(body=json.dumps({'result': False, "msg": "Failed to Clone that repository"}),mimetype="application/json")

            except Exception as e:
                return func.HttpResponse(body=json.dumps({'result': False, "msg": "Failed to Clone that repository"}),mimetype="application/json")

            # Change cwd back to parent folder
            os.chdir('..')
        else:
            print(f"The directory 'uploads/{apiName}' already exists.")
        # Parse each file and scan for functions
        functions = scan_python_files(apiName)

        # Delete uploaded API files
        logging.info("Deleting {} files...".format(apiName))
        if os.path.isdir('uploads/{}'.format(apiName)):
            shutil.rmtree('uploads/{}'.format(apiName))

        return func.HttpResponse(body=json.dumps({'result': True, "msg": json.dumps(functions)}), mimetype="application/json")
    except CosmosHttpResponseError:
        message = CosmosHttpResponseErrorMessage()
        logging.error(message)
        return func.HttpResponse(body=json.dumps({'result': False, "msg": message}), mimetype="application/json")