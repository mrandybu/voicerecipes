from voiceserver import app, mail
from flask import request
from voiceserver.server_funcs import ServerFunctions
from voiceserver.db_funcs import DBFuncs
import json
from flask_mail import Message


class Server(object):
    def __init__(self, query=None, reg_data=None):
        self.query = query
        if reg_data:
            json_data = json.loads(reg_data)
            self.login = json_data['login']
            self.password = json_data['password']
            self.email = json_data['email']

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


@app.route('/recipes/<recipe_name>')
def get_request(recipe_name=None):
    server = Server(recipe_name)
    return server.request_to_vk()


@app.route('/checkin', methods=['POST'])
def check_in():
    if request.method == 'POST':
        server = Server(reg_data=request.data)
        return server.set_registration()


@app.route('/sendcode/<email>/<code>')
def send_confirm_code(email, code):
    msg = Message('Confirmation code to VoiceRecipes',
                  recipients=[email])
    msg.html = "<p>Hello! We are glad to welcome you in VoiceRecipes! " \
               "Your confirmation code: %s</p>" % code
    try:
        mail.send(msg)
        return 'ok'
    except:
        pass


if __name__ == '__main__':
    app.run()
