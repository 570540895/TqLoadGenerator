import datetime

import requests
import json
from utils import sendRequest, queryMysql
import pymysql

with open('./template/request_body_template.json', 'r') as fp:
    d = json.load(fp)
    fp.close()

with open('./template/request_headers_template.json', 'r') as fp:
    headers_json = json.load(fp)
    fp.close()

with open('./config/mysql-config.json', 'r') as fp:
    mySql_config_dict = json.load(fp)
    i = 1
    mysql_kwargs = {
        'host': mySql_config_dict['host'],
        'port': mySql_config_dict['port'],
        'user': mySql_config_dict['user'],
        'password': mySql_config_dict['password'],
        'database': mySql_config_dict['database'],
        'charset': mySql_config_dict['charset']
    }
    fp.close()

'''
d['resource'] = {
    "projectUuid": "b34b40f9-9861-4234-ae3e-030cd7f8eddb",
    "computeSpecUuid": "439d33e6-cabd-4ebf-b99b-4178ffc15c64",
    "computeSpecName": "toby-test",
    "workerNum": 1
}
'''
data = queryMysql.query_mysql(**mysql_kwargs)
for d in data:
    print(int(datetime.datetime.timestamp(d[1])))


""""
response = sendRequest.send_request('http://10.200.88.230:32380/api/model/trainjobs', 'post', headers_json, d)
# response = requests.post('http://10.200.88.230:32380/api/model/trainjobs',  json=d, headers=headers)
print(response)
"""
