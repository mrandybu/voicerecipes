import requests
import json
from database.orm_db import User
import os
import __root__


class TestDataBase(object):
    def __init__(self, test_type):
        self.subfile = __root__ \
            .get_root_path_to_file('subfile.json')
        self.reg_data = {
            'login': 'test',
            'password': 'test123',
            'email': 'test@test.com'
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
        req = requests.post('http://127.0.0.1:5000/checkin', json.dumps(self.reg_data))
        if req.ok:
            return req.text
        return 'Local server error!'

    @staticmethod
    def get_all_data():
        return User.query.all()

    def get_test(self):
        tests_kit = {
            'remreg': self.test_remote_registration,
            'locreg': self.test_local_registration,
            'alldata': self.get_all_data
        }
        return tests_kit[self.test_type]()


def init_test():
    test = TestDataBase('alldata')
    return test.get_test()


if __name__ == '__main__':
    print(init_test())
