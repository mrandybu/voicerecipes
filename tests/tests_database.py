import requests
import json
from database.orm_db import User
import os
import __root__
from voiceserver.server import Server


class TestDataBase(object):
    def __init__(self, test_type):
        self.subfile = __root__ \
            .get_root_path_to_file('subfile.json')
        self.reg_data = {
            'login': 'test',
            'password': 'test123',
            'email': 'your@email.com'
        }
        self.test_type = test_type

    def test_remote_registration(self):
        with open(self.subfile) as sbf:
            server_host = json.load(sbf)['server']

        url = os.path.join(server_host, 'checkin')
        req = requests.post(url, json.dumps(self.reg_data))
        if req.ok:
            return req.text
        return 'Remote server error!'

    def test_local_registration(self):
        req = requests.post('http://127.0.0.1:5000/checkin',
                            json.dumps(self.reg_data))
        if req.ok:
            return req.text
        return req.text

    def test_send_code_local(self):
        reg_data = json.dumps(self.reg_data)
        Server(reg_data=reg_data)
        req = requests.get('http://127.0.0.1:5000/sendcode/{}/{}'
                           .format(self.reg_data['email'], '1331'))
        if req.ok:
            return req.text
        return 'Error method!'

    @staticmethod
    def get_all_data():
        return User.query.all()

    def get_test(self):
        tests_kit = {
            'remreg': self.test_remote_registration,
            'locreg': self.test_local_registration,
            'alldata': self.get_all_data,
            'sendcode': self.test_send_code_local
        }
        return tests_kit[self.test_type]()


def init_test():
    test = TestDataBase('sendcode')
    return test.get_test()


if __name__ == '__main__':
    print(init_test())
