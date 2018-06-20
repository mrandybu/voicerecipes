from voiceserver import app
from flask import request
from voiceserver.server_funcs import ServerFunctions
from voiceserver.db_funcs import DBFuncs
import json


class Server(object):
    def __init__(self, query=None, reg_data=None, auth=None, save_data=None):
        self.query = query
        self.auth = auth
        self.save_data = save_data
        if reg_data:
            json_data = json.loads(reg_data)
            self.login = json_data['login']
            self.password = json_data['password']
            self.email = json_data['email']
        if auth:
            json_data = json.loads(auth)
            self.login = json_data['login']
            self.password = json_data['password']

    def request_to_vk(self):
        get_server = ServerFunctions(self.query)
        recipes_list = get_server.preprocessing_recipe_text()
        return recipes_list

    def set_registration(self):
        new_user = DBFuncs(
            self.login,
            self.password,
            self.email
        )
        set_reg = new_user.check_in()
        return set_reg

    def auth_user(self):
        auth = DBFuncs(
            self.login,
            self.password,
            None
        )
        return auth.auth_user()

    def save_recipe(self):
        save = DBFuncs(None, None, None, self.save_data)
        return save.save_recipe()


@app.route('/recipes/<recipe_name>')
def get_request(recipe_name=None):
    server = Server(recipe_name)
    return server.request_to_vk()


@app.route('/checkin', methods=['POST'])
def check_in():
    if request.method == 'POST':
        server = Server(reg_data=request.data)
        return server.set_registration()


@app.route('/auth', methods=['POST'])
def auth_user():
    if request.method == 'POST':
        server = Server(auth=request.data)
        return server.auth_user()


@app.route('/saverecipe', methods=['POST'])
def save_recipe():
    if request.method == 'POST':
        server = Server(save_data=request.data)
        return server.save_recipe()


if __name__ == '__main__':
    app.run()
