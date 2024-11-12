import datetime
import json
import threading
import time
from utils import getToken, queryMysql, sendRequest

tq_config_file = './config/tq-config.json'
mysql_config_file = './config/mysql-config.json'
headers_template_file = './template/request_headers_template.json'

# read config files
with open(tq_config_file, 'r') as fp:
    tq_config_dict = json.load(fp)
    tq_host = tq_config_dict['host']
    tq_port = tq_config_dict['port']
    compute_spec_list = tq_config_dict['computeSpecList']
    # tq_user_name = tq_config_dict['tqUserName']
    fp.close()
base_url = 'http://' + tq_host + ':' + tq_port

with open(mysql_config_file, 'r') as fp:
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
tq_token = getToken.get_tq_token(base_url)

# read config json
with open(headers_template_file, 'r') as fp:
    headers_json = json.load(fp)
    headers_json['Authorization'] = 'tqToken={}'.format(tq_token)
    fp.close()


def stop_all():
    mysql_rows = queryMysql.query_mysql(**mysql_kwargs)
    for row in mysql_rows:
        uuid = row[0]
        stop_api_path = '/api/model/trainjobs/{}/stop'.format(uuid)
        request_url = base_url + stop_api_path
        threading.Timer(0, sendRequest.send_request, args=[request_url, 'put', headers_json]).start()


if __name__ == '__main__':
    stop_all()
