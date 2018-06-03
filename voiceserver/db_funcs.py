from database.orm_db import User, db
import hashlib
import uuid
import re


class DBFuncs(object):
    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

    def check_in(self):
        try:
            salt = uuid.uuid4().hex
            hash_pass = hashlib.md5((self.password + salt).encode()).hexdigest()
            new_user = User(login=self.login, password=hash_pass, email=self.email)
            db.session.add(new_user)
            db.session.commit()
            return 'Successfully registered!'
        except Exception as err:
            reg = re.compile('UNIQUE.*failed')
            if len(re.findall(reg, str(err))) != 0:
                return 'User already exists!'
        return 'Unknown error!'
