from database.orm_db import db, User, Recipe, UsersRecipes
import hashlib
import uuid
import re
import random
import __root__
import json
import smtplib


class DBFuncs(object):
    def __init__(self, login, password, email, save_data=None):
        self.login = login
        self.password = password
        self.email = email
        self.save_data = save_data
        self.confirm_code = random.randrange(1000, 10000)
        self.subfile = __root__.get_root_path_to_file('subfile.json')

    def check_in(self):
        request_json = self.requests_json()
        try:
            salt = uuid.uuid4().hex
            hash_pass = hashlib.md5((self.password + salt).encode()).hexdigest()
            new_user = User(login=self.login, password=hash_pass, email=self.email, salt=salt)
            db.session.add(new_user)
            db.session.commit()
            confirm_code = self.send_confirm_code()
            if confirm_code:
                return _jd(self.requests_json(confirm_code)['all_ok'])
            else:
                return _jd(request_json['reg_ok'])
        except Exception as err:
            reg = re.compile('UNIQUE.*failed')
            if len(re.findall(reg, str(err))) != 0:
                return _jd(request_json['exists'])
        return _jd(request_json['fail'])

    def send_confirm_code(self):
        confirm_code = self.confirm_code
        try:
            with open(self.subfile) as sbf:
                mail = json.load(sbf)['mail']
            server = smtplib.SMTP(mail['host'], mail['port'])
            server.starttls()
            server.login(mail['login'], mail['password'])
            content_mail = 'Hello! We are glad to welcome you in VoiceRecipes!\n \
            Your confirmation code: %d' % confirm_code
            body_mail = "\r\n".join((
                "From: %s" % mail['login'],
                "To: %s" % self.email,
                "Subject: %s" % 'VoiceRecipes confirmation email',
                "",
                content_mail
            ))
            server.sendmail(mail['login'], self.email, body_mail)
            server.quit()
        except:
            pass
        return confirm_code

    def auth_user(self):
        request_json = self.requests_json()
        try:
            user = User.query.filter_by(login=self.login).first()
            if user:
                hash_get_pass = hashlib.md5((self.password + user.salt).encode()).hexdigest()
                if hash_get_pass == user.password:
                    return _jd(request_json['auth_ok'])
                else:
                    return _jd(request_json['auth_bad'])
            return _jd(request_json['not_exist'])
        except:
            return _jd(request_json['serv_err'])

    def save_recipe(self):
        request_json = self.requests_json()
        save_data = json.load(self.save_data)
        user_id = User.query.filter_by(login=save_data['login']).first().id
        recipe = Recipe(title=save_data['title'],
                        ingredients=save_data['ing'],
                        cook=save_data['cook'],
                        time=save_data['time'],
                        hard=save_data['hard'])
        try:
            db.session.add(recipe)
            db.session.commit()
        except:
            return _jd(request_json['save_err'])
        users_recipes = UsersRecipes(user_id=user_id, recipe_id=recipe.id)
        try:
            db.session.add(users_recipes)
            db.session.commit()
        except:
            return _jd(request_json['serv_err'])
        return _jd(request_json['save_ok'])

    @staticmethod
    def requests_json(arg=None):
        request_json = {
            'all_ok': {
                'request': 'reg ok, code ok, %s' % str(arg)
            },
            'reg_ok': {
                'request': 'reg ok, code fail'
            },
            'fail': {
                'request': 'reg fail'
            },
            'exists': {
                'request': 'user exists'
            },
            'auth_ok': {
                'request': 'auth ok'
            },
            'auth_bad': {
                'request': 'auth bad'
            },
            'not_exist': {
                'request': 'user not exist'
            },
            'serv_err': {
                'request': 'server err'
            },
            'save_err': {
                'request': 'save err'
            },
            'save_ok': {
                'request': 'save ok'
            },
        }
        return request_json


def _jd(json_):
    return json.dumps(json_)
