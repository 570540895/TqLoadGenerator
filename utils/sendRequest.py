import json
import requests


def send_request(url, method, headers, body=None):
    if method == 'post':
        response = requests.post(url, headers=headers, json=body).text
    elif method == 'get':
        response = requests.get(url, headers=headers).text
    elif method == 'put':
        response = requests.put(url, headers=headers).text
    elif method == 'delete':
        response = requests.delete(url, headers=headers).text
    elif method == 'patch':
        response = requests.patch(url, headers=headers).text
    else:
        response = ''
    # print('response: {}'.format(json.loads(response)))
    return json.loads(response)
