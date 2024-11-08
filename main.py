import copy
import datetime
import json
import logging
import multiprocessing
import pandas as pd
import sys
import threading
import time
from utils import getToken, preProcess, queryMysql, sendRequest

is_debug = True if sys.gettrace() else False

# log config
log_file = './logs/log-{}.log'.format(datetime.date.today())
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)

# generate tasks params
csv_file = './data/data.csv' if not is_debug else './data/data_test.csv'
sorted_csv_file = './data/sorted_data.csv' if not is_debug else './data/sorted_data_test.csv'
gen_api_path = '/api/model/trainjobs'
time_compress = 30
start_interval = 10

# stop tasks params

# config params
tq_config_file = './config/tq-config.json'
mysql_config_file = './config/mysql-config.json'
headers_template_file = './template/request_headers_template.json'
body_template_file = './template/request_body_template.json'

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


# generate tq jobs
def gen_jobs(m_duration, s_dict, s_lock):
    request_url = base_url + gen_api_path

    # sort csv file
    preProcess.sort_csv_file(csv_file, sorted_csv_file)

    m_duration.value = preProcess.get_min_duration(sorted_csv_file) if not is_debug else 3

    # read template files
    with open(headers_template_file, 'r') as fp:
        headers_json = json.load(fp)
        headers_json['Authorization'] = 'tqToken={}'.format(tq_token)
        fp.close()

    with open(body_template_file, 'r') as fp:
        body_json = json.load(fp)
        fp.close()

    # create tasks according to csv file
    df = pd.read_csv(sorted_csv_file)

    csv_start_time = df['createDate'][0]
    exec_start_time = int(time.time()) + start_interval

    for index, row in df.iterrows():
        name_prefix = 'tq-test' if not is_debug else 'toby-test'
        task_name = name_prefix + str(index)
        create_date = row['createDate']
        exec_duration = max(int(row['exec_duration'] / time_compress), 1) if not is_debug else 10
        gpu_num = row['gpu_num']
        worker_num = row['worker_num']

        body = copy.deepcopy(body_json)
        body['name'] = task_name
        if gpu_num == 1:
            body['resource']['projectUuid'] = compute_spec_list[0]['projectUuid']
            body['resource']['computeSpecUuid'] = compute_spec_list[0]['computeSpecUuid']
            body['resource']['computeSpecName'] = compute_spec_list[0]['computeSpecName']
        elif gpu_num == 4:
            body['resource']['projectUuid'] = compute_spec_list[1]['projectUuid']
            body['resource']['computeSpecUuid'] = compute_spec_list[1]['computeSpecUuid']
            body['resource']['computeSpecName'] = compute_spec_list[1]['computeSpecName']
        elif gpu_num == 8:
            body['resource']['projectUuid'] = compute_spec_list[2]['projectUuid']
            body['resource']['computeSpecUuid'] = compute_spec_list[2]['computeSpecUuid']
            body['resource']['computeSpecName'] = compute_spec_list[2]['computeSpecName']
        else:
            log.error('generate tasks error: index: {} gpu_num is {}.'.format(index, gpu_num))
            continue
        body['resource']['workerNum'] = worker_num

        time_interval = int((create_date - csv_start_time) / time_compress)
        threading.Timer(exec_start_time + time_interval - int(time.time()),
                        sendRequest.send_request, args=[request_url, 'post', headers_json, body]).start()
        if is_debug:
            print('scheduled task name: {} time: {}'.format(task_name, time_interval))
        with s_lock:
            s_dict[task_name] = exec_duration


# stop tq jobs
def stop_jobs(m_duration, s_dict, s_lock):
    # read config json
    with open(headers_template_file, 'r') as fp:
        headers_json = json.load(fp)
        headers_json['Authorization'] = 'tqToken={}'.format(tq_token)
        fp.close()

    while True:
        mysql_rows = queryMysql.query_mysql(**mysql_kwargs)
        for row in mysql_rows:
            uuid = row[0]
            task_name = row[1]
            start_time = int(datetime.datetime.timestamp(row[2]))
            now = int(time.time())
            if task_name not in s_dict:
                # log.error('Task: {} not found in generated tasks set while stopping task'.format(task_name))
                continue
            stop_api_path = '/api/model/trainjobs/{}/stop'.format(uuid)
            request_url = base_url + stop_api_path
            threading.Timer(start_time+s_dict[task_name]-now,
                            sendRequest.send_request, args=[request_url, 'put', headers_json]).start()
            with s_lock:
                del s_dict[task_name]
        time.sleep(max(m_duration.value - 1, 3))


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        min_duration = multiprocessing.Value('i', 10)
        shared_dict = manager.dict()
        lock = multiprocessing.Lock()
        p1 = multiprocessing.Process(target=gen_jobs, args=(min_duration, shared_dict, lock, ))
        p2 = multiprocessing.Process(target=stop_jobs, args=(min_duration, shared_dict, lock, ))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

