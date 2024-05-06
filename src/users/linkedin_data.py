import requests
import json
from src.users.constants import URL_API, API_KEY

def get_user_data(email: str):

    querystring = {f"apikey": {API_KEY}, "email": {email}}

    response = requests.request("GET", URL_API, params=querystring)

    json_object = json.loads(response.text)

    json_str = json.dumps(json_object, indent=4)

    return json_object