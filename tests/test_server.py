import requests
import json
from voiceserver.api_for_vk import GetVkApi
import __root__


def test_vk_api():
    query = 'каша'.encode('utf-8')
    new_request = GetVkApi(query=query, count=10)
    response = new_request.search_recipes()
    print(response)


def test_local_server():
    http_request = 'recipes/рыба'
    url = 'http://127.0.0.1:5000/'
    query = url + http_request
    new_request = requests.get(query)
    if new_request.ok:
        response = new_request.text
        #print(response)
    else:
        print('error of request')


def test_remote_server():
    subfile = __root__.get_root_path_to_file('subfile.json')
    with open(subfile) as sbf:
        server_host = (json.load(sbf))['server']
    http_request = 'recipes/рыба'
    query = server_host + http_request
    new_request = requests.get(query)
    if new_request.ok:
        response = new_request.text
        print(response)
    else:
        print('request error!')


if __name__ == '__main__':
    # test_remote_server()
    test_local_server()
    # test_vk_api()
