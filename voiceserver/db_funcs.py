from database.orm_db import User, db
import hashlib
import uuid
import re
import random
import requests
import __root__
import os
import json


class DBFuncs(object):
    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email
        self.confirm_code = random.randrange(1000, 10000)
        self.subfile = __root__.get_root_path_to_file('subfile.json')

    def check_in(self):
        request_json = self.requests_json()
        try:
            salt = uuid.uuid4().hex
            hash_pass = hashlib.md5((self.password + salt).encode()).hexdigest()
            new_user = User(login=self.login, password=hash_pass, email=self.email)
            db.session.add(new_user)
            db.session.commit()
            if self.send_confirm_code() == 'ok':
                return _jd(request_json['all_ok'])
            else:
                return _jd(request_json['reg_ok'])
        except Exception as err:
            reg = re.compile('UNIQUE.*failed')
            if len(re.findall(reg, str(err))) != 0:
                return _jd(request_json['exists'])
        return _jd(request_json['fail'])

    def send_confirm_code(self):
        with open(self.subfile) as sbf:
            server_host = (json.load(sbf))['server']
        url = os.path.join(server_host, 'sendcode',
                           self.email, str(self.confirm_code))
        req = requests.get(url)
        if req.ok:
            return req.text

    @staticmethod
    def requests_json():
        request_json = {
            'all_ok': {
                'request': 'registration ok, code ok'
            },
            'reg_ok': {
                'request': 'registration ok, code fail'
            },
            'fail': {
                'request': 'registration fail'
            },
            'exists': {
                'request': 'user exists'
            },
        }
        return request_json


def _jd(json_):
    return json.dumps(json_)
