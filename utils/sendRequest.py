import requests
import json


def send_request(url, method, headers, body):
    if method == 'post':
        response = requests.post(url, headers=headers, json=body).text
    elif method == 'get':
        response = requests.get(url, headers=headers).text
    elif method == 'put':
        response = requests.put(url, headers=headers).text
    elif method == 'delete':
        response = requests.delete(url, headers=headers).text
    else:
        response = ''
    return json.loads(response)
