from voiceserver import app
from flask import request
from voiceserver.server_funcs import ServerFunctions
from voiceserver.db_funcs import DBFuncs
import json


class Server(object):
    def __init__(self, query=None, reg_data=None):
        self.query = query
        self.reg_data = reg_data

    def request_to_vk(self):
        get_server = ServerFunctions(self.query)
        recipes_list = get_server.preprocessing_recipe_text()
        return recipes_list

    def set_registration(self):
        json_data = json.loads(self.reg_data)
        new_user = DBFuncs(
            json_data['login'],
            json_data['password'],
            json_data['email']
        )
        set_reg = new_user.check_in()
        return set_reg


@app.route('/recipes/<recipe_name>')
def get_request(recipe_name=None):
    server = Server(recipe_name)
    return server.request_to_vk()


@app.route('/checkin', methods=['POST'])
def check_in():
    if request.method == 'POST':
        server = Server(reg_data=request.data)
        return server.set_registration()


if __name__ == '__main__':
    app.run()
