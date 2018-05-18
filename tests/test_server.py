import requests, json
from voiceserver.api_for_vk import GetVkApi


def test_vk_api():
    query = 'каша'.encode('utf-8')
    new_request = GetVkApi(query=query, count=10)
    response = new_request.search_recipes()
    print(response)


def test_local_server():
    name = 'каша'
    url = 'http://127.0.0.1:5000/recipes/'
    query = url + name
    new_request = requests.get(query)
    if new_request.ok:
        response = new_request.text
        print(response)
    else:
        print('error of request')


def test_remote_server():
    with open('subfile.json') as subfile:
        server_host = json.load(subfile)
    query = 'каша'.encode('utf-8')
    new_request = requests.post(server_host['server'], query)
    if new_request.ok:
        response = new_request.text
        print(response)
    else:
        print('request error!')


if __name__ == '__main__':
    # test_remote_server()
    test_local_server()
    # test_vk_api()
