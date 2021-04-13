POLISH_ZLOTY = {
    'code': 'pln',
    'name': 'Polish Zloty',
    'plural': 'Polish zlotys',
    'symbol': 'zł',
    'symbol_native': 'zł'
}

DEFAULT_IP_LOCALIZATIONS = [
    {
        'currency': 1,
        'url': 'http://www.facebook.com/',
        'ip': '9.9.9.9',
        'type': 'ipv4',
        'latitude': '0.0000000000000',
        'longitude': '0.0000000000000'},
    {
        'currency': 1,
        'url': 'http://www.fanfare.com',
        'ip': '1.2.7.9',
        'type': 'ipv4',
        'latitude': '1.0000000000000',
        'longitude': '1.0000000000000'},
    {
        'currency': 1,
        'url': 'http://www.twarzoksiazka.com/',
        'ip': '2a03:2880:f103:83:face:b00c:0:25de',
        'type': 'ipv6',
        'latitude': '3.0000000000000',
        'longitude': '3.0000000000000'
    }
]

import http.client
import json

_token_url = '/api/token/'
_local_host = '127.0.0.1:8000'


def _get_tokens(username, password):
    connection = http.client.HTTPConnection(_local_host)
    auth_payload = json.dumps({'username': username, 'password': password})

    connection.request("POST", _token_url, headers={"Content-Type":  "application/json"}, body=auth_payload)
    response = connection.getresponse().read().decode('utf-8')

    return json.loads(response)


if __name__ == '__main__':
    username = ''
    password = ''

    token_dict = _get_tokens(username, password)
    token = token_dict['access']

    headers = {"Content-Type":  "application/json", 'Authorization': f"Bearer {token}"}
    connection = http.client.HTTPConnection(_local_host)

    connection.request("POST", url='/api/currency/', headers=headers, body=json.dumps(POLISH_ZLOTY))

    connection = http.client.HTTPConnection(_local_host)
    connection.request("GET", url='/api/currency/1', headers=headers)
    print(connection.getresponse().read().decode('utf-8'))

    connection = http.client.HTTPConnection(_local_host)
    connection.request("POST", url='/api/localizations/', headers=headers, body=json.dumps(DEFAULT_IP_LOCALIZATIONS))

    connection = http.client.HTTPConnection(_local_host)
    connection.request("GET", url='/api/localizations/1', headers=headers)
    print(connection.getresponse().read().decode('utf-8'))
