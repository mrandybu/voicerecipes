import requests
import json
import os
import __root__
from voiceserver.db_funcs import DBFuncs
from database.orm_db import User, db


class TestDataBase(object):
    def __init__(self, test_type):
        self.subfile = __root__ \
            .get_root_path_to_file('subfile.json')
        self.reg_data = {
            'login': 'test',
            'password': 'test123',
            'email': 'guneriled@gmail.com'
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
        user = User.query.filter_by(login=self.reg_data['login']).first()
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            pass
        req = requests.post('http://127.0.0.1:5000/checkin',
                            json.dumps(self.reg_data))
        if req.ok:
            return req.text
        return req.text

    def test_send_code_local(self):
        reg_data = json.dumps(self.reg_data)
        func = DBFuncs('gun22', '123', 'guneriled@gmail.com')
        return func.send_confirm_code()

    def test_send_code_remote(self):
        with open(self.subfile) as sbf:
            host = json.load(sbf)['server']
        reg_data = json.dumps(self.reg_data)
        req = requests.get(os.path.join(host, 'sendcode', 'guneriled@gmail.com', '1234'))

        if req.ok:
            return req.text
        return 'Error method'

    def test_auth_local(self):
        url = os.path.join('http://127.0.0.1:5000/', 'auth')
        req = requests.post(url, json.dumps(self.reg_data))
        if req.ok:
            return req.text
        return 'Error method..('

    def test_auth_rem(self):
        with open(self.subfile) as sbf:
            host = json.load(sbf)['server']
        url = os.path.join(host, 'auth')
        req = requests.post(url, json.dumps(self.reg_data))
        if req.ok:
            return req.text
        return 'Error method..('

    def test_save_recipe(self):
        with open(self.subfile) as sbf:
            host = json.load(sbf)['server']
        url = os.path.join(host, 'saverecipe')
        save_data = {
            'login': 'test',
            'title': 'Test title',
            'ing': 'Test ingredients',
            'cook': 'Test cook',
            'time': 'Test time',
            'hard': 'Test hard',
        }
        req = requests.post(url, json.dumps(save_data))
        if req.ok:
            return req.text
        return 'Error method..('

    @staticmethod
    def get_all_data():
        return User.query.all()

    def get_test(self):
        tests_kit = {
            'remreg': self.test_remote_registration,
            'locreg': self.test_local_registration,
            'alldata': self.get_all_data,
            'locmail': self.test_send_code_local,
            'remail': self.test_send_code_remote,
            'authloc': self.test_auth_local,
            'authrem': self.test_auth_rem,
            'saverec': self.test_save_recipe,
        }
        return tests_kit[self.test_type]()


def init_test():
    test = TestDataBase('saverec')
    return test.get_test()


if __name__ == '__main__':
    print(init_test())
