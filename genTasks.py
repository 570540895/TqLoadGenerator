import logging
import json
import time
import pandas as pd
import sched
from utils import preProcess, sendRequest

log_file = r'logs/test.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger(__name__)

csv_file = r'data/data.csv'
sorted_csv_file = r'data/sorted_data.csv'

config_file = r'config/config.json'
headers_template_file = r'./template/request_headers_template.json'
body_template_file = r'./template/request_body_template.json'

api_path = r'/api/model/trainjobs'

time_compress = 30
start_interval = 30


def run():
    # read config file
    with open(config_file, 'r') as fp:
        config_dict = json.load(fp)
        host = config_dict['host']
        port = config_dict['port']
        computeSpecList = config_dict['computeSpecList']
        # tq_user_name = config_dict['tqUserName']
        fp.close()
    base_url = 'http://' + host + ':' + port
    request_url = base_url + api_path

    # sort csv file
    preProcess.sort_csv_file(csv_file, sorted_csv_file)

    # read template files
    with open(headers_template_file, 'r') as fp:
        headers_json = json.load(fp)
        fp.close()

    with open(body_template_file, 'r') as fp:
        body_json = json.load(fp)
        fp.close()

    # create tasks according to csv file
    df = pd.read_csv(sorted_csv_file)

    csv_start_time = df['createDate'][0]
    exec_start_time = int(time.time()) + start_interval

    scheduler = sched.scheduler(time.time, time.sleep)

    for index, row in df.iterrows():
        task_name = 'tq_test_' + str(index)
        create_date = row['createDate']
        exec_duration = row['exec_duration']
        gpu_num = row['gpu_num']
        worker_num = row['worker_num']

        body_json['name'] = task_name
        if gpu_num == 4:
            body_json['resource']['projectUuid'] = computeSpecList[0]['projectUuid']
            body_json['resource']['computeSpecUuid'] = computeSpecList[0]['computeSpecUuid']
            body_json['resource']['computeSpecName'] = computeSpecList[0]['computeSpecName']
        elif gpu_num == 8:
            body_json['resource']['projectUuid'] = computeSpecList[1]['projectUuid']
            body_json['resource']['computeSpecUuid'] = computeSpecList[1]['computeSpecUuid']
            body_json['resource']['computeSpecName'] = computeSpecList[1]['computeSpecName']
        else:
            log.error('gpu_num is not 4 or 8.')
            continue
        body_json['resource']['workerNum'] = worker_num

        time_interval = int((create_date - csv_start_time) / time_compress)
        scheduler.enter(exec_start_time+time_interval-int(time.time()), 0,
                        sendRequest.send_request, (request_url, 'post', headers_json, body_json))


if __name__ == '__main__':
    run()
