import requests
import json
from utils import sendRequest
import pymysql

with open('./template/request_body_template.json', 'r') as fp:
    d = json.load(fp)
    fp.close()

with open('./template/request_headers_template.json', 'r') as fp:
    headers_json = json.load(fp)
    fp.close()

with open('./config/mysql-config.json', 'r') as fp:
    mysql_config_dict = json.load(fp)
    mysql_kwargs = {
        'host': mysql_config_dict['host'],
        'port': mysql_config_dict['port'],
        'user': mysql_config_dict['user'],
        'password': mysql_config_dict['password'],
        'database': mysql_config_dict['database'],
        'charset': mysql_config_dict['charset']
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
db = pymysql.connections.Connection(**mysql_kwargs)
cur = db.cursor()
sql = "select * from job_info where status = 'running';"
try:
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
except Exception as e:
    print(e)
cur.close()
db.close()


""""
response = sendRequest.send_request('http://10.200.88.230:32380/api/model/trainjobs', 'post', headers_json, d)
# response = requests.post('http://10.200.88.230:32380/api/model/trainjobs',  json=d, headers=headers)
print(response)
"""
