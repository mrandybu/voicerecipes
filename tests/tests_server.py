import requests
import json
from voiceserver.api_for_vk import GetVkApi
import __root__


class TestsSever(object):
    def __init__(self, test_type, query):
        self.subfile = __root__.get_root_path_to_file('subfile.json')
        self.test_type = test_type
        self.query = query

    def test_vk_api(self):
        query = self.query.encode('utf-8')
        new_request = GetVkApi(query=query, count=10)
        response = new_request.search_recipes()
        print(response)

    def test_local_server(self):
        http_request = 'recipes/' + self.query
        url = 'http://127.0.0.1:5000/'
        query = url + http_request
        new_request = requests.get(query)
        if new_request.ok:
            response = new_request.text
            print(response)
        else:
            print('error of request')

    def test_remote_server(self):
        with open(self.subfile) as sbf:
            server_host = (json.load(sbf))['server']
        http_request = 'recipes/' + self.query
        query = server_host + http_request
        new_request = requests.get(query)
        if new_request.ok:
            response = new_request.text
            print(response)
        else:
            print('request error!')

    def get_test(self):
        tests_kit = {
            'vkapi': self.test_vk_api,
            'locserv': self.test_local_server,
            'remserv': self.test_remote_server
        }
        tests_kit[self.test_type]()


def init_test():
    test = TestsSever('locserv', 'рыба')
    test.get_test()


if __name__ == '__main__':
    init_test()
