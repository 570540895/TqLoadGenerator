import requests
import json
from utils import sendRequest

with open('./template/request_body_template.json', 'r') as fp:
    d = json.load(fp)
    fp.close()

with open('./template/request_headers_template.json', 'r') as fp:
    headers_json = json.load(fp)
    fp.close()

'''
d['resource'] = {
    "projectUuid": "b34b40f9-9861-4234-ae3e-030cd7f8eddb",
    "computeSpecUuid": "439d33e6-cabd-4ebf-b99b-4178ffc15c64",
    "computeSpecName": "toby-test",
    "workerNum": 1
}
'''

response = sendRequest.send_request('http://10.200.88.230:32380/api/model/trainjobs', 'post', headers_json, d)
# response = requests.post('http://10.200.88.230:32380/api/model/trainjobs',  json=d, headers=headers)
print(response)

