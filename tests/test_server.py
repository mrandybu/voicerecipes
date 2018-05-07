import requests, json
from voiceserver.api_for_vk import GetVkApi


def test_vk_api():
    query = 'десерты'
    new_request = GetVkApi(query=query, count=10)
    response = new_request.search_recipes()
    print(response)


def test_local_server():
    recipe_name = 'десерты'
    url = 'http://127.0.0.1:5000/recipes/'
    query = url + recipe_name
    new_request = requests.get(query)
    if new_request.ok:
        response = new_request.text
        print(response)
    else:
        print('Error request to local server!')


def test_remote_server():
    with open('subfile.json') as subfile:
        server_host = json.load(subfile)
    recipe_name = 'десерты'
    query = server_host['server'] + recipe_name
    new_request = requests.get(query)
    if new_request.ok:
        response = new_request.text
        print(response)
    else:
        print('Error request to remote server!')


if __name__ == '__main__':
    test_remote_server()
    test_local_server()
