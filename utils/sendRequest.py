import json
import logging as log
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
    res_json = json.loads(response)
    if 'code' in res_json:
        if res_json['code'] == 200:
            log.info('successfully send request url: {}.'.format(url))
        else:
            log.error('failed send request url: {}, error msg: {}'.format(url, res_json['msg']))
    else:
        log.error('code not found in http response')
    return res_json
