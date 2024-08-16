import requests
import json
import warnings
import os
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # Correct import statement
from tinydb import TinyDB, Query
from tinydb.operations import increment

# Suppress only the InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Configuration variables
ZVM_ADDRESS = os.getenv("ZVM_ADDRESS", "172.16.50.100")
ZVM_USERNAME = os.getenv("ZVM_USERNAME", "admin")
ZVM_PASSWORD = os.getenv("ZVM_PASSWORD", "Zertodata987!")
VERIFY_CERTIFICATE = os.getenv("VERIFY_CERTIFICATE", "False").lower() in ('true', '1', 't')

# Nothing below should need modified for the example to run and list VPGs

KEYCLOAK_API_BASE = f"https://{ZVM_ADDRESS}/auth/realms/zerto/protocol/openid-connect/token"
ZVM_API_BASE = f"https://{ZVM_ADDRESS}/v1/"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize TinyDB database
db = TinyDB('db.json')
events_table = db.table('events')
tasks_table = db.table('tasks')

#function to get a token from keycloak
def get_token():
    uri = KEYCLOAK_API_BASE
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'username': ZVM_USERNAME,
        'password': ZVM_PASSWORD,
        'grant_type': 'password',
        'client_id': 'zerto-client'  # This is typically required for the password grant
    }

    try:
        response = requests.post(uri, headers=headers, data=body, verify=VERIFY_CERTIFICATE)
        response.raise_for_status()
        token_data = response.json()
        logging.debug(f"Got Token Data: {token_data}")
        return token_data.get('access_token')
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        logging.error(f"Error obtaining token: {e}")
        return None

# main function which executes when the program is run
def run():

    # authenticate to the zvm
    token = get_token()
    if not token:
        logging.error("Failed to get token.")
        return

    # events section
    # this line can be adjusted to any API url in ZVM
    uri = f"{ZVM_API_BASE}events"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    body = {}

    try:
        # this line will need to be modified depending on if the api you want is a GET, POST, PUT, DELETE, etc
        response = requests.get(uri, headers=headers, json=body, verify=VERIFY_CERTIFICATE)
        response.raise_for_status()
        logging.debug(f'Request successful.\n')
        logging.debug(f'{response.json()}')

        # Iterate over the events and store the identifiers
        for event in response.json():
            identifier = event.get('EventIdentifier')
            if identifier:
                logging.debug(f'Processing Event - {identifier}')
                
                # Search the tinydb to see if this event already exists
                Event = Query()
                if events_table.contains(Event.identifier == identifier):
                    logging.debug(f'Event {identifier} already exists in the database.')
                    continue  # Skip to the next event if this one is already in the database
                
                # If the event isn't already in the database, print that it's a new event 
                # and the event JSON details. Then add the EventIdentifier to the database.
                logging.debug(f'New Event detected: {identifier}')
                logging.debug(f'Event details: {json.dumps(event, indent=2)}')
                logging.info(f'{event.get("OccurredOn")} | {identifier} | {event.get("UserName")} | {event.get("Description")} | {event.get("SiteName")} | {event.get("SiteIdentifier")}')
                
                # Insert the identifier into the TinyDB
                events_table.insert({'identifier': identifier})
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Zerto API failed: {e}")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return


    # tasks section
    # this line can be adjusted to any API url in ZVM
    uri = f"{ZVM_API_BASE}tasks"

    try:
        # this line will need to be modified depending on if the api you want is a GET, POST, PUT, DELETE, etc
        response = requests.get(uri, headers=headers, json=body, verify=VERIFY_CERTIFICATE)
        response.raise_for_status()
        logging.debug(f'Request successful.\n')
        logging.debug(f'{response.json()}')

        # Iterate over the events and store the identifiers
        for task in response.json():
            identifier = task.get('TaskIdentifier')
            if identifier:
                logging.debug(f'Processing Task - {identifier}')
                
                # Search the tinydb to see if this event already exists
                Task = Query()
                if tasks_table.contains(Task.identifier == identifier):
                    logging.debug(f'Task {identifier} already exists in the database.')
                    continue  # Skip to the next event if this one is already in the database
                
                # If the event isn't already in the database, print that it's a new event 
                # and the event JSON details. Then add the EventIdentifier to the database.
                logging.debug(f'New Task detected: {identifier}')
                logging.debug(f'Task details: {json.dumps(task, indent=2)}')
                # Assuming `task` is the current dictionary object representing the JSON task
                site_identifier = task.get("RelatedEntities", {}).get("Sites", [{}])[0].get("identifier")

                # Then use it in your logging statement
                logging.info(f'{task.get("started")} | {identifier} | {task.get("InitiatedBy")} | {task.get("Type")} | {site_identifier} | {task.get("TaskIdentifier")}')

                # Insert the identifier into the TinyDB
                tasks_table.insert({'identifier': identifier})
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Zerto API failed: {e}")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return


if __name__ == '__main__':
    run()
