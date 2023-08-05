import requests
import json



def permission_list(api_key:str):

    url = "http://localhost:8000/user-api-permission-name"

    payload = {}
    headers = {
        'api-key': api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def permission(permission_name:int, api_key:str):
    url = "http://localhost:8000/user-api-permission-name/"
    payload = json.dumps({
        "permission_name": permission_name
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json


def assign_user_permission(
        permission_id:int, 
        user_id:int, 
        read_permission:bool, 
        write_permission:bool, 
        edit_permission:bool, 
        delete_permission:bool,
        api_key:str
    ):
    url = "http://localhost:8000/user-api-permission/"

    payload = json.dumps({
        "permission_id": int(permission_id),
        "user_id": int(user_id),
        "read_permission": read_permission,
        "write_permission": write_permission,
        "edit_permission": edit_permission,
        "delete_permission": delete_permission
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def update_user_permission(
        permission_id:int,  
        read_permission:bool, 
        write_permission:bool, 
        edit_permission:bool, 
        delete_permission:bool,
        api_key:str
        ):

    url = f"http://localhost:8000/edit-user-permission/{permission_id}/"

    payload = json.dumps({
        "read_permission": read_permission,
        "write_permission": write_permission,
        "edit_permission": edit_permission,
        "delete_permission": delete_permission
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response.json()


def delete_user_permission(permission_id:int, api_key:str):
    url = "http://localhost:8000/delete-user-permission/"

    payload = json.dumps({
        "user_permission_id": permission_id
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json()


def delete_permission(permission_id:int, api_key:str):
    url = "http://localhost:8000/delete-permission/"

    payload = json.dumps({
        "permission_id": permission_id
    })
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    return response.json()


