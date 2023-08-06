import requests
import json
base_url = 'http://authpackage.pythonanywhere.com'

def create_user(email:str, first_name:str, last_name:str, password:str, api_key:str):

    url = f"{base_url}/user-api/"

    payload = json.dumps({
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def user_list(api_key:str):

    url = f"{base_url}/user-api/"

    payload = {}
    headers = {
        'api-key': api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def get_single_user(user_id:int, api_key:str):

    url = f"{base_url}/user-api/{user_id}/"

    payload = {}
    headers = {
        'api-key': api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def delete_user(user_id:int, api_key:str):
 
    url = f"{base_url}/delete-user/"

    payload = json.dumps({
        "user_id": user_id
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json()


def authenticate_user(email:str, password:str, api_key:str):
    url = f"{base_url}/authenticate-user/"

    payload = json.dumps({
        "email": email,
        "password": password
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


