import logging
import json
from utils import sendRequest

api_path = '/api/users/refreshToken'
rf_token_cfg_file = '../config/tq-refresh-token.json' if __name__ == '__main__' else './config/tq-refresh-token.json '
log_file = '../logs/test.log' if __name__ == '__main__' else './logs/test.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_tq_token(base_url):
    with open(rf_token_cfg_file, 'r') as fp:
        d = json.load(fp)
        tq_refresh_token = d['tqRefreshToken']
        fp.close()

    request_url = base_url + api_path
    headers = {'Authorization': 'tqRefreshToken={}'.format(tq_refresh_token)}
    response = sendRequest.send_request(request_url, 'patch', headers=headers)
    if 'code' not in response:
        log.error("Response code not found when get token.")
        raise
    if response['code'] != 200:
        log.error('Error when get token: code:{}, msg:{}'.format(response['code'], response['msg']))
        raise
    return response['data']['tqToken']


if __name__ == '__main__':
    print(get_tq_token('http://10.200.88.230:32380'))
