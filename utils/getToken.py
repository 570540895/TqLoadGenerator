import json
import sendRequest

api_path = '/api/users/refreshToken'
tq_refresh_token_config_file = '../config/tq-refresh-token.json'


def get_tq_token(base_url):
    with open(tq_refresh_token_config_file, 'r') as fp:
        d = json.load(fp)
        tq_refresh_token = d['tqRefreshToken']
        fp.close()

    request_url = base_url + api_path
    headers = {'Authorization': 'tqRefreshToken={}'.format(tq_refresh_token)}
    response = sendRequest.send_request(request_url, 'patch', headers=headers)
    return response['data']['tqToken']


if __name__ == '__main__':
    print(get_tq_token('http://10.200.88.230:32380'))
