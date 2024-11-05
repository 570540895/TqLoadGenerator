import logging
import json
import requests

log_file = r'logs/test.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger(__name__)


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
    r_dict = json.loads(response)
    if 'code' not in r_dict:
        log.error("response code not found")
    return json.loads(response)
